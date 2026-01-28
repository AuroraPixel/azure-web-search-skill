"""测试客户端连接和基本功能"""

import sys
import os

# 设置 Windows 控制台编码为 UTF-8
if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)
    except:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# 使用 force_terminal=True 避免编码问题
console = Console(force_terminal=True, legacy_windows=False)


def test_imports():
    """测试模块导入"""
    console.print("\n[cyan][TEST 1] 检查模块导入...[/cyan]")
    try:
        from src.config import get_settings, setup_env_file
        from src.logger import setup_logger
        from src.web_search import AzureWebSearch
        from src.models import SearchMode, WebSearchResult
        console.print("[green][OK] 所有模块导入成功[/green]")
        return True
    except ImportError as e:
        console.print(f"[red][FAIL] 模块导入失败：{e}[/red]")
        return False


def test_env_file():
    """测试环境文件"""
    console.print("\n[cyan][TEST 2] 检查环境配置文件...[/cyan]")
    try:
        from src.config import setup_env_file
        if not setup_env_file():
            console.print("[yellow][WARN] .env 文件未找到，请先配置[/yellow]")
            return False
        console.print("[green][OK] .env 文件存在[/green]")
        return True
    except Exception as e:
        console.print(f"[red][FAIL] 环境文件检查失败：{e}[/red]")
        return False


def test_config_loading():
    """测试配置加载"""
    console.print("\n[cyan][TEST 3] 加载配置...[/cyan]")
    try:
        from src.config import get_settings
        settings = get_settings()
        
        # 显示配置信息（隐藏敏感信息）
        config_table = Table(show_header=False, box=None)
        config_table.add_column("配置项", style="cyan")
        config_table.add_column("值", style="yellow")
        
        config_table.add_row("API Key", f"{settings.azure_openai_api_key[:8]}..." if len(settings.azure_openai_api_key) > 8 else "***")
        config_table.add_row("Endpoint", settings.azure_openai_endpoint)
        config_table.add_row("Model", settings.azure_openai_model)
        config_table.add_row("API Version", settings.azure_openai_api_version)
        config_table.add_row("Country", settings.web_search_country or "未设置")
        config_table.add_row("Log Level", settings.log_level)
        
        console.print(config_table)
        console.print("[green][OK] 配置加载成功[/green]")
        return settings
    except Exception as e:
        console.print(f"[red][FAIL] 配置加载失败：{e}[/red]")
        console.print("\n[yellow][HINT] 常见问题：[/yellow]")
        console.print("  1. 检查 .env 文件是否存在")
        console.print("  2. 检查必填字段是否都已填写：")
        console.print("     - AZURE_OPENAI_API_KEY")
        console.print("     - AZURE_OPENAI_ENDPOINT")
        return None


def test_client_init(settings):
    """测试客户端初始化"""
    console.print("\n[cyan][TEST 4] 初始化客户端...[/cyan]")
    try:
        from src.logger import setup_logger
        from src.web_search import AzureWebSearch
        
        # 设置日志
        setup_logger(level=settings.log_level)
        
        # 创建客户端
        search_client = AzureWebSearch(settings)
        console.print("[green][OK] 客户端初始化成功[/green]")
        return search_client
    except Exception as e:
        console.print(f"[red][FAIL] 客户端初始化失败：{e}[/red]")
        console.print("\n[yellow][HINT] 可能的原因：[/yellow]")
        console.print("  1. API Key 无效")
        console.print("  2. Endpoint 格式不正确")
        console.print("  3. 网络连接问题")
        return None


def test_basic_search(search_client):
    """测试基本搜索功能"""
    console.print("\n[cyan][TEST 5] 执行简单搜索...[/cyan]")
    
    test_query = "帮我查询clawdbot最新的使用技巧"
    console.print(f"[dim]测试查询：{test_query}[/dim]")
    
    try:
        console.print("[yellow][WAIT] 正在搜索（可能需要几秒钟）...[/yellow]")
        
        # 执行快速搜索
        result = search_client.quick_search(test_query)
        
        # 显示结果统计
        stats_table = Table(show_header=False, box=None)
        stats_table.add_column("指标", style="cyan")
        stats_table.add_column("值", style="yellow")
        
        stats_table.add_row("返回文本长度", f"{len(result.text)} 字符")
        stats_table.add_row("引用数量", str(len(result.citations)))
        stats_table.add_row("搜索调用次数", str(len(result.search_calls)))
        stats_table.add_row("唯一来源", str(len(result.get_unique_sources())))
        
        console.print(stats_table)
        
        # 显示部分结果
        if result.text:
            preview = result.text[:200] + "..." if len(result.text) > 200 else result.text
            console.print(Panel(preview, title="结果预览", border_style="green"))
        
        console.print("[green][OK] 搜索功能正常[/green]")
        return True
    except Exception as e:
        console.print(f"[red][FAIL] 搜索失败：{e}[/red]")
        console.print("\n[yellow][HINT] 可能的原因：[/yellow]")
        console.print("  1. API Key 无效或过期")
        console.print("  2. 模型部署名称不正确")
        console.print("  3. Web Search 功能未启用")
        console.print("  4. 网络连接问题")
        console.print("  5. 配额不足")
        
        # 显示详细错误信息
        import traceback
        console.print("\n[red]详细错误信息：[/red]")
        console.print(traceback.format_exc())
        return False


def main():
    """主测试函数"""
    console.print(Panel.fit(
        "[bold cyan]Azure Web Search 客户端测试[/bold cyan]\n"
        "测试客户端配置和基本功能",
        border_style="cyan"
    ))
    
    # 测试结果跟踪
    tests_passed = 0
    tests_total = 5
    
    # 测试 1：模块导入
    if not test_imports():
        console.print("\n[red][FAIL] 基础测试失败，无法继续[/red]")
        sys.exit(1)
    tests_passed += 1
    
    # 测试 2：环境文件
    if not test_env_file():
        console.print("\n[red][FAIL] 请先配置 .env 文件[/red]")
        console.print("[yellow][HINT] 运行以下命令：[/yellow]")
        console.print("   copy env.example .env")
        console.print("   然后编辑 .env 文件填写您的配置")
        sys.exit(1)
    tests_passed += 1
    
    # 测试 3：配置加载
    settings = test_config_loading()
    if not settings:
        console.print("\n[red][FAIL] 配置加载失败，无法继续[/red]")
        sys.exit(1)
    tests_passed += 1
    
    # 测试 4：客户端初始化
    search_client = test_client_init(settings)
    if not search_client:
        console.print("\n[red][FAIL] 客户端初始化失败，无法继续[/red]")
        sys.exit(1)
    tests_passed += 1
    
    # 测试 5：基本搜索
    if test_basic_search(search_client):
        tests_passed += 1
    
    # 显示总结
    console.print("\n" + "=" * 60)
    if tests_passed == tests_total:
        console.print(Panel(
            f"[bold green][SUCCESS] 所有测试通过！({tests_passed}/{tests_total})[/bold green]\n\n"
            "客户端工作正常，可以开始使用！\n\n"
            "下一步：\n"
            "  • 运行交互式程序：python main.py\n"
            "  • 查看示例：python examples/basic_search.py\n"
            "  • 阅读文档：README.md",
            title="测试完成",
            border_style="green"
        ))
        sys.exit(0)
    else:
        console.print(Panel(
            f"[bold yellow][WARNING] 部分测试失败 ({tests_passed}/{tests_total})[/bold yellow]\n\n"
            "请检查上方的错误信息并修复问题",
            title="测试完成",
            border_style="yellow"
        ))
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow][WARN] 测试已中断[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red][ERROR] 未预期的错误：{e}[/red]")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)
