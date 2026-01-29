"""配置模块测试"""

import pytest
from pydantic import ValidationError

from src.config import Settings


def test_settings_validation():
    """测试配置验证"""
    # 有效配置
    settings = Settings(
        azure_openai_api_key="test-key",
        azure_openai_endpoint="https://test.openai.azure.com",
        _env_file=None,
    )
    assert settings.azure_openai_api_key == "test-key"
    assert settings.azure_openai_endpoint == "https://test.openai.azure.com"


def test_endpoint_validation():
    """测试 Endpoint 验证"""
    # 应该自动移除末尾斜杠
    settings = Settings(
        azure_openai_api_key="test-key",
        azure_openai_endpoint="https://test.openai.azure.com/",
    )
    assert settings.azure_openai_endpoint == "https://test.openai.azure.com"

    # 无效的 Endpoint（缺少协议）
    with pytest.raises(ValidationError):
        Settings(
            azure_openai_api_key="test-key",
            azure_openai_endpoint="test.openai.azure.com",
        )


def test_country_code_validation():
    """测试国家代码验证"""
    # 有效的国家代码
    settings = Settings(
        azure_openai_api_key="test-key",
        azure_openai_endpoint="https://test.openai.azure.com",
        web_search_country="us",  # 小写会自动转换为大写
    )
    assert settings.web_search_country == "US"

    # 无效的国家代码（长度不对）
    with pytest.raises(ValidationError):
        Settings(
            azure_openai_api_key="test-key",
            azure_openai_endpoint="https://test.openai.azure.com",
            web_search_country="USA",
        )


def test_log_level_validation():
    """测试日志级别验证"""
    # 有效的日志级别
    settings = Settings(
        azure_openai_api_key="test-key",
        azure_openai_endpoint="https://test.openai.azure.com",
        log_level="debug",  # 小写会自动转换为大写
    )
    assert settings.log_level == "DEBUG"

    # 无效的日志级别
    with pytest.raises(ValidationError):
        Settings(
            azure_openai_api_key="test-key",
            azure_openai_endpoint="https://test.openai.azure.com",
            log_level="INVALID",
        )


def test_default_values(monkeypatch):
    """测试默认值"""
    # 避免外部环境变量影响默认值断言
    monkeypatch.delenv("AZURE_OPENAI_MODEL", raising=False)
    monkeypatch.delenv("AZURE_OPENAI_API_VERSION", raising=False)
    monkeypatch.delenv("WEB_SEARCH_COUNTRY", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    settings = Settings(
        azure_openai_api_key="test-key",
        azure_openai_endpoint="https://test.openai.azure.com",
        _env_file=None,
    )
    assert settings.azure_openai_model == "gpt-4o"
    assert settings.azure_openai_api_version == "2024-12-01-preview"
    assert settings.log_level == "INFO"
    assert settings.web_search_country is None
