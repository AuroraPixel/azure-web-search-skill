"""数据模型测试"""

from src.models import (
    SearchMode,
    URLCitation,
    UserLocation,
    WebSearchResult,
    WebSearchTool,
)


def test_search_mode_enum():
    """测试搜索模式枚举"""
    assert SearchMode.QUICK.value == "quick"
    assert SearchMode.AGENTIC.value == "agentic"


def test_url_citation():
    """测试 URL 引用模型"""
    citation = URLCitation(
        start_index=0,
        end_index=10,
        url="https://example.com",
        title="Example",
    )
    assert citation.type == "url_citation"
    assert citation.url == "https://example.com"
    assert citation.title == "Example"


def test_user_location():
    """测试用户位置模型"""
    location = UserLocation(country="US")
    assert location.type == "approximate"
    assert location.country == "US"


def test_web_search_tool():
    """测试 Web 搜索工具模型"""
    # 不带位置
    tool = WebSearchTool()
    tool_dict = tool.to_dict()
    assert tool_dict["type"] == "web_search_preview"
    assert "user_location" not in tool_dict

    # 带位置
    tool = WebSearchTool(user_location=UserLocation(country="CN"))
    tool_dict = tool.to_dict()
    assert tool_dict["type"] == "web_search_preview"
    assert tool_dict["user_location"]["country"] == "CN"


def test_web_search_result():
    """测试搜索结果模型"""
    citations = [
        URLCitation(
            start_index=0,
            end_index=10,
            url="https://example.com",
            title="Example 1",
        ),
        URLCitation(
            start_index=20,
            end_index=30,
            url="https://example.com",  # 重复的 URL
            title="Example 1 Again",
        ),
        URLCitation(
            start_index=40,
            end_index=50,
            url="https://another.com",
            title="Example 2",
        ),
    ]

    result = WebSearchResult(
        text="Test result",
        citations=citations,
    )

    # 测试获取唯一源
    unique_sources = result.get_unique_sources()
    assert len(unique_sources) == 2  # 应该只有 2 个唯一的 URL
    assert unique_sources[0]["url"] == "https://example.com"
    assert unique_sources[1]["url"] == "https://another.com"
