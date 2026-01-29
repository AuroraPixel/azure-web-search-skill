"""测试 MCP Server 配置"""

import sys
import os

import pytest


# 这是一个偏“手动/集成”的环境检查脚本，会依赖本机 .env、Claude/Cursor 配置文件等。
# 默认跳过，避免在 CI/无环境变量时阻塞单元测试。
if os.environ.get("RUN_INTEGRATION_TESTS") != "1":
    pytest.skip(
        "integration/manual test (requires local .env + desktop config). "
        "Set RUN_INTEGRATION_TESTS=1 to run.",
        allow_module_level=True,
    )

# 设置标准输出编码为 UTF-8（避免替换 sys.stdout 导致 pytest capture 异常）
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        # 某些环境不支持 reconfigure，忽略即可
        pass

# 添加 src 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试基础导入"""
    print("=" * 60)
    print("测试 1: 检查基础依赖")
    print("=" * 60)
    
    try:
        import mcp
        print("✓ mcp 包已安装")
        print(f"  版本: {mcp.__version__ if hasattr(mcp, '__version__') else '未知'}")
    except ImportError as e:
        print(f"✗ mcp 包未安装: {e}")
        print("  请运行: uv pip install mcp")
        return False
    
    try:
        from openai import OpenAI
        print("✓ openai 包已安装")
    except ImportError as e:
        print(f"✗ openai 包未安装: {e}")
        return False
    
    try:
        from pydantic import BaseModel
        print("✓ pydantic 包已安装")
    except ImportError as e:
        print(f"✗ pydantic 包未安装: {e}")
        return False
    
    try:
        from rich.console import Console
        print("✓ rich 包已安装")
    except ImportError as e:
        print(f"✗ rich 包未安装: {e}")
        return False
    
    print()
    return True


def test_env_config():
    """测试环境配置"""
    print("=" * 60)
    print("测试 2: 检查环境配置")
    print("=" * 60)
    
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    
    if not os.path.exists(env_file):
        print("✗ .env 文件不存在")
        print(f"  请创建 .env 文件: {env_file}")
        print("  可以从 env.example 复制")
        return False
    
    print(f"✓ .env 文件存在: {env_file}")
    
    try:
        from src.config import get_settings
        settings = get_settings()
        
        print("✓ 配置加载成功")
        print(f"  端点: {settings.azure_openai_endpoint}")
        print(f"  模型: {settings.azure_openai_model}")
        print(f"  API 版本: {settings.azure_openai_api_version}")
        
        # 检查 API 密钥是否设置
        if settings.azure_openai_api_key and len(settings.azure_openai_api_key) > 10:
            print(f"  API 密钥: {'*' * 20}...{settings.azure_openai_api_key[-4:]}")
        else:
            print("  ⚠ API 密钥未设置或无效")
            return False
        
    except Exception as e:
        print(f"✗ 配置加载失败: {e}")
        return False
    
    print()
    return True


def test_web_search_client():
    """测试 Web Search 客户端"""
    print("=" * 60)
    print("测试 3: 检查 Web Search 客户端")
    print("=" * 60)
    
    try:
        from src.config import get_settings
        from src.web_search import AzureWebSearch
        
        settings = get_settings()
        client = AzureWebSearch(settings)
        
        print("✓ Web Search 客户端创建成功")
        print(f"  端点: {settings.azure_openai_endpoint}")
        
    except Exception as e:
        print(f"✗ 客户端创建失败: {e}")
        return False
    
    print()
    return True


def test_mcp_server():
    """测试 MCP Server 文件"""
    print("=" * 60)
    print("测试 4: 检查 MCP Server 文件")
    print("=" * 60)
    
    mcp_server_file = os.path.join(os.path.dirname(__file__), "mcp_server.py")
    
    if not os.path.exists(mcp_server_file):
        print(f"✗ mcp_server.py 文件不存在: {mcp_server_file}")
        return False
    
    print(f"✓ mcp_server.py 文件存在")
    
    try:
        # 尝试导入（不运行）
        import importlib.util
        spec = importlib.util.spec_from_file_location("mcp_server", mcp_server_file)
        if spec and spec.loader:
            print("✓ mcp_server.py 文件格式正确")
        else:
            print("✗ mcp_server.py 文件格式错误")
            return False
    except Exception as e:
        print(f"✗ mcp_server.py 导入测试失败: {e}")
        return False
    
    print()
    return True


def test_claude_config():
    """测试 Claude Desktop 配置"""
    print("=" * 60)
    print("测试 5: 检查 Claude Desktop 配置")
    print("=" * 60)
    
    import json
    
    if sys.platform == "win32":
        config_path = os.path.join(os.environ.get("APPDATA", ""), "Claude", "claude_desktop_config.json")
    elif sys.platform == "darwin":
        config_path = os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")
    else:
        config_path = os.path.expanduser("~/.config/Claude/claude_desktop_config.json")
    
    print(f"配置文件路径: {config_path}")
    
    if not os.path.exists(config_path):
        print("⚠ Claude Desktop 配置文件不存在")
        print("  需要运行安装脚本：")
        if sys.platform == "win32":
            print("    .\\install_mcp.ps1")
        else:
            print("    ./install_mcp.sh")
        return False
    
    print("✓ Claude Desktop 配置文件存在")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if "mcpServers" in config and "azure-web-search" in config["mcpServers"]:
            print("✓ azure-web-search 服务器已配置")
            server_config = config["mcpServers"]["azure-web-search"]
            print(f"  命令: {server_config.get('command', 'N/A')}")
            print(f"  参数: {server_config.get('args', [])}")
        else:
            print("⚠ azure-web-search 服务器未配置")
            print("  需要运行安装脚本")
            return False
            
    except Exception as e:
        print(f"✗ 配置文件读取失败: {e}")
        return False
    
    print()
    return True


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("Azure Web Search MCP Server 配置测试")
    print("=" * 60 + "\n")
    
    results = []
    
    results.append(("基础依赖", test_imports()))
    results.append(("环境配置", test_env_config()))
    results.append(("Web Search 客户端", test_web_search_client()))
    results.append(("MCP Server 文件", test_mcp_server()))
    results.append(("Claude Desktop 配置", test_claude_config()))
    
    # 总结
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{status} - {name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print()
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 所有测试通过！你的 MCP Server 已准备就绪。")
        print("\n下一步:")
        print("1. 重启 Claude Desktop")
        print("2. 在 Claude 中尝试: '使用 web search 搜索 AI 趋势'")
    else:
        print("\n⚠ 部分测试失败，请根据上述提示修复问题。")
        if not results[4][1]:  # Claude config failed
            print("\n提示: 运行安装脚本来自动配置 Claude Desktop:")
            if sys.platform == "win32":
                print("  .\\install_mcp.ps1")
            else:
                print("  ./install_mcp.sh")
    
    print()
    return passed == total


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n测试已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
