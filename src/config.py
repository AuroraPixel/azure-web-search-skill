"""配置管理模块"""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用程序设置"""

    # Azure OpenAI 配置
    azure_openai_api_key: str = Field(..., description="Azure OpenAI API Key")
    azure_openai_endpoint: str = Field(..., description="Azure OpenAI Endpoint URL")
    azure_openai_model: str = Field(default="gpt-4o", description="模型部署名称")
    azure_openai_api_version: str = Field(
        default="2024-12-01-preview", description="API 版本"
    )

    # Web Search 配置
    web_search_country: Optional[str] = Field(
        default=None, description="用户位置国家代码（ISO 3166-1 alpha-2）"
    )

    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("azure_openai_endpoint")
    @classmethod
    def validate_endpoint(cls, v: str) -> str:
        """验证并规范化 endpoint"""
        v = v.strip()
        if not v.startswith(("http://", "https://")):
            raise ValueError("Endpoint 必须以 http:// 或 https:// 开头")
        # 移除末尾的斜杠
        return v.rstrip("/")

    @field_validator("web_search_country")
    @classmethod
    def validate_country_code(cls, v: Optional[str]) -> Optional[str]:
        """验证国家代码"""
        if v is None:
            return v
        v = v.strip().upper()
        if len(v) != 2:
            raise ValueError("国家代码必须是 2 个字符（ISO 3166-1 alpha-2）")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """验证日志级别"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"日志级别必须是以下之一：{', '.join(valid_levels)}")
        return v


def get_settings() -> Settings:
    """获取应用程序设置"""
    return Settings()


def setup_env_file():
    """设置环境变量文件"""
    env_file = Path(".env")
    env_example = Path("env.example")

    if not env_file.exists() and env_example.exists():
        print("⚠️  未找到 .env 文件")
        print(f"📝 请复制 {env_example} 为 .env 并填写您的配置")
        print(f"   命令：cp {env_example} .env")
        return False
    return True
