"""快速测试搜索功能"""

import sys
import os

# 设置 Windows 控制台编码
if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)
    except:
        pass

from rich.console import Console

console = Console(force_terminal=True, legacy_windows=False)

def quick_test():
    """快速测试"""
    console.print("[cyan]正在测试客户端...[/cyan]\n")
    
    try:
        from src.config import get_settings, setup_env_file
        from src.logger import setup_logger
        from src.web_search import AzureWebSearch
        
        # 检查环境文件
        if not setup_env_file():
            console.print("[red]请先配置 .env 文件[/red]")
            return False
        
        # 加载配置
        settings = get_settings()
        console.print("[green][OK] 配置加载成功[/green]")
        
        # 设置日志（降低日志级别，避免干扰输出）
        setup_logger(level="WARNING")
        
        # 创建客户端
        search_client = AzureWebSearch(settings)
        console.print("[green][OK] 客户端初始化成功[/green]")
        
        # 执行搜索
        query = "帮我查询clawdbot最新的使用技巧"
        console.print(f"\n[cyan]搜索查询：{query}[/cyan]")
        console.print("[yellow]正在搜索...[/yellow]\n")
        
        result = search_client.quick_search(query)
        
        # 显示结果
        console.print("[green]搜索完成！[/green]\n")
        console.print("=" * 60)
        console.print("[bold]搜索结果：[/bold]\n")
        console.print(result.text[:500] + "..." if len(result.text) > 500 else result.text)
        console.print("\n" + "=" * 60)
        console.print(f"[yellow]引用数量：{len(result.citations)}[/yellow]")
        console.print(f"[yellow]搜索调用：{len(result.search_calls)}[/yellow]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]错误：{e}[/red]")
        import traceback
        console.print(traceback.format_exc())
        return False


if __name__ == "__main__":
    try:
        success = quick_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n[yellow]已取消[/yellow]")
        sys.exit(1)
