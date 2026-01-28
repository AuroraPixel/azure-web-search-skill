"""Azure OpenAI Web Search 核心模块"""

from typing import Any, Dict, List, Optional

from openai import OpenAI

from .config import Settings
from .logger import get_logger
from .models import (
    CodeInterpreterTool,
    Message,
    MessageContent,
    SearchAction,
    SearchMode,
    URLCitation,
    UserLocation,
    WebSearchCall,
    WebSearchResult,
    WebSearchTool,
)

logger = get_logger(__name__)


class AzureWebSearch:
    """Azure OpenAI Web Search 客户端"""

    def __init__(self, settings: Settings):
        """
        初始化 Web Search 客户端

        Args:
            settings: 应用程序设置
        """
        self.settings = settings
        self.client = OpenAI(
            api_key=settings.azure_openai_api_key,
            base_url=f"{settings.azure_openai_endpoint}/openai/v1/",
        )
        logger.info(f"🚀 已连接到 Azure OpenAI: {settings.azure_openai_endpoint}")

    def _build_tools(
        self,
        mode: SearchMode,
        country: Optional[str] = None,
        include_code_interpreter: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        构建工具配置

        Args:
            mode: 搜索模式
            country: 国家代码
            include_code_interpreter: 是否包含代码解释器工具

        Returns:
            工具配置列表
        """
        tools = []

        # 添加 Web Search 工具
        web_search_tool = WebSearchTool(type="web_search_preview")

        # 如果指定了国家代码，添加位置信息
        if country:
            web_search_tool.user_location = UserLocation(type="approximate", country=country)

        tools.append(web_search_tool.to_dict())

        # Deep Research 模式下可以添加代码解释器
        if mode == SearchMode.DEEP_RESEARCH and include_code_interpreter:
            code_tool = CodeInterpreterTool()
            tools.append(code_tool.to_dict())

        return tools

    def _parse_response(self, response: Any) -> WebSearchResult:
        """
        解析响应数据

        Args:
            response: API 响应对象

        Returns:
            解析后的搜索结果
        """
        # 获取原始响应数据
        raw_data = response.model_dump() if hasattr(response, "model_dump") else {}

        output_items = getattr(response, "output", [])

        search_calls = []
        messages = []

        # 解析输出项
        for item in output_items:
            item_type = getattr(item, "type", None)

            if item_type == "web_search_call":
                # 解析搜索调用
                action_data = getattr(item, "action", {})
                if hasattr(action_data, "model_dump"):
                    action_dict = action_data.model_dump()
                else:
                    action_dict = {
                        "type": getattr(action_data, "type", "search"),
                        "query": getattr(action_data, "query", None),
                        "domains": getattr(action_data, "domains", None),
                    }

                search_call = WebSearchCall(
                    id=getattr(item, "id", ""),
                    status=getattr(item, "status", "completed"),
                    action=SearchAction(**action_dict),
                )
                search_calls.append(search_call)

            elif item_type == "message":
                # 解析消息
                content_list = []
                for content in getattr(item, "content", []):
                    if getattr(content, "type", None) == "output_text":
                        annotations = []
                        for ann in getattr(content, "annotations", []):
                            if getattr(ann, "type", None) == "url_citation":
                                citation = URLCitation(
                                    start_index=getattr(ann, "start_index", 0),
                                    end_index=getattr(ann, "end_index", 0),
                                    url=getattr(ann, "url", ""),
                                    title=getattr(ann, "title", None),
                                )
                                annotations.append(citation)

                        msg_content = MessageContent(
                            text=getattr(content, "text", ""), annotations=annotations
                        )
                        content_list.append(msg_content)

                if content_list:
                    message = Message(
                        id=getattr(item, "id", ""),
                        status=getattr(item, "status", "completed"),
                        role=getattr(item, "role", "assistant"),
                        content=content_list,
                    )
                    messages.append(message)

        # 提取文本和引用
        text = ""
        citations = []

        if messages:
            first_message = messages[0]
            if first_message.content:
                text = first_message.content[0].text
                citations = first_message.content[0].annotations

        return WebSearchResult(
            text=text, citations=citations, search_calls=search_calls, raw_response=raw_data
        )

    def search(
        self,
        query: str,
        mode: SearchMode = SearchMode.QUICK,
        country: Optional[str] = None,
        model: Optional[str] = None,
        include_code_interpreter: bool = False,
    ) -> WebSearchResult:
        """
        执行 Web 搜索

        Args:
            query: 搜索查询
            mode: 搜索模式
            country: 国家代码（可选）
            model: 模型名称（可选，默认使用配置中的模型）
            include_code_interpreter: 是否包含代码解释器（仅 Deep Research 模式）

        Returns:
            搜索结果
        """
        # 使用配置中的国家代码（如果未指定）
        if country is None:
            country = self.settings.web_search_country

        # 使用配置中的模型（如果未指定）
        if model is None:
            model = self.settings.azure_openai_model

        # Deep Research 模式需要使用 o3-deep-research 模型
        if mode == SearchMode.DEEP_RESEARCH:
            model = "o3-deep-research"

        # 构建工具配置
        tools = self._build_tools(mode, country, include_code_interpreter)

        logger.info(f"🔍 开始搜索：{query}")
        logger.info(f"📊 模式：{mode.value}")
        if country:
            logger.info(f"🌍 国家：{country}")

        try:
            # 调用 API
            response = self.client.responses.create(
                model=model, tools=tools, input=query
            )

            # 解析响应
            result = self._parse_response(response)

            logger.info(f"✅ 搜索完成，找到 {len(result.citations)} 个引用")

            return result

        except Exception as e:
            logger.error(f"❌ 搜索失败：{e}")
            raise

    def quick_search(
        self, query: str, country: Optional[str] = None
    ) -> WebSearchResult:
        """
        快速搜索（无推理）

        Args:
            query: 搜索查询
            country: 国家代码（可选）

        Returns:
            搜索结果
        """
        return self.search(query, mode=SearchMode.QUICK, country=country)

    def agentic_search(
        self, query: str, country: Optional[str] = None
    ) -> WebSearchResult:
        """
        智能体搜索（带推理）

        Args:
            query: 搜索查询
            country: 国家代码（可选）

        Returns:
            搜索结果
        """
        return self.search(query, mode=SearchMode.AGENTIC, country=country)

    def deep_research(
        self,
        query: str,
        country: Optional[str] = None,
        include_code_interpreter: bool = False,
    ) -> WebSearchResult:
        """
        深度研究

        Args:
            query: 研究主题
            country: 国家代码（可选）
            include_code_interpreter: 是否包含代码解释器工具

        Returns:
            研究结果
        """
        return self.search(
            query,
            mode=SearchMode.DEEP_RESEARCH,
            country=country,
            include_code_interpreter=include_code_interpreter,
        )
