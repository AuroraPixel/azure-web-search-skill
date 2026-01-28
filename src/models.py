"""数据模型定义"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SearchMode(str, Enum):
    """搜索模式"""

    QUICK = "quick"  # 快速搜索（无推理）
    AGENTIC = "agentic"  # 智能体搜索（带推理）
    DEEP_RESEARCH = "deep_research"  # 深度研究


class SearchActionType(str, Enum):
    """搜索动作类型"""

    SEARCH = "search"
    OPEN_PAGE = "open_page"
    FIND_IN_PAGE = "find_in_page"


class URLCitation(BaseModel):
    """URL 引用"""

    type: str = "url_citation"
    start_index: int = Field(description="引用在文本中的起始位置")
    end_index: int = Field(description="引用在文本中的结束位置")
    url: str = Field(description="引用的 URL")
    title: Optional[str] = Field(default=None, description="页面标题")


class SearchAction(BaseModel):
    """搜索动作"""

    type: SearchActionType = Field(description="动作类型")
    query: Optional[str] = Field(default=None, description="搜索查询")
    domains: Optional[List[str]] = Field(default=None, description="搜索的域名列表")


class WebSearchCall(BaseModel):
    """Web 搜索调用"""

    id: str = Field(description="调用 ID")
    type: str = "web_search_call"
    status: str = Field(description="调用状态")
    action: SearchAction = Field(description="执行的动作")


class MessageContent(BaseModel):
    """消息内容"""

    type: str = "output_text"
    text: str = Field(description="消息文本")
    annotations: List[URLCitation] = Field(
        default_factory=list, description="文本中的 URL 引用"
    )


class Message(BaseModel):
    """消息"""

    id: str = Field(description="消息 ID")
    type: str = "message"
    status: str = Field(description="消息状态")
    role: str = Field(description="角色（如：assistant）")
    content: List[MessageContent] = Field(description="消息内容列表")


class WebSearchResult(BaseModel):
    """Web 搜索结果"""

    text: str = Field(description="搜索结果文本")
    citations: List[URLCitation] = Field(default_factory=list, description="引用列表")
    search_calls: List[WebSearchCall] = Field(default_factory=list, description="搜索调用列表")
    raw_response: Optional[Dict[str, Any]] = Field(default=None, description="原始响应数据")

    def get_unique_sources(self) -> List[Dict[str, str]]:
        """获取唯一的引用源列表"""
        seen_urls = set()
        sources = []

        for citation in self.citations:
            if citation.url not in seen_urls:
                seen_urls.add(citation.url)
                sources.append(
                    {
                        "url": citation.url,
                        "title": citation.title or citation.url,
                    }
                )

        return sources


class UserLocation(BaseModel):
    """用户位置"""

    type: str = "approximate"
    country: str = Field(description="国家代码（ISO 3166-1 alpha-2）")


class WebSearchTool(BaseModel):
    """Web 搜索工具配置"""

    type: str = "web_search_preview"
    user_location: Optional[UserLocation] = Field(default=None, description="用户位置")

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {"type": self.type}
        if self.user_location:
            result["user_location"] = {
                "type": self.user_location.type,
                "country": self.user_location.country,
            }
        return result


class CodeInterpreterTool(BaseModel):
    """代码解释器工具配置"""

    type: str = "code_interpreter"
    container: Dict[str, str] = Field(default_factory=lambda: {"type": "auto"})

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {"type": self.type, "container": self.container}
