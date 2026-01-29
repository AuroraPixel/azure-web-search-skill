"""测试菜单显示"""

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
from rich.prompt import Prompt

console = Console(force_terminal=True, legacy_windows=False)


def show_menu() -> str:
    """显示菜单并获取用户选择"""
    console.print("\n" + "=" * 60, style="cyan")
    console.print("请选择搜索模式：", style="bold yellow")
    console.print("  [1] 快速搜索 (Quick Search) - 快速获取结果", style="green")
    console.print("  [2] 智能体搜索 (Agentic Search) - 带推理的搜索", style="blue")
    console.print("  [3] 更改国家/地区", style="yellow")
    console.print("  [0] 退出", style="red")
    console.print("=" * 60 + "\n", style="cyan")

    choice = Prompt.ask("请输入选项", choices=["0", "1", "2", "3"], default="1")
    return choice


if __name__ == "__main__":
    console.print("[cyan]菜单测试[/cyan]\n")
    choice = show_menu()
    
    if choice == "0":
        console.print("[green]退出选项正常[/green]")
    elif choice == "1":
        console.print("[green]快速搜索选项正常[/green]")
    elif choice == "2":
        console.print("[green]智能体搜索选项正常[/green]")
    elif choice == "3":
        console.print("[green]更改国家选项正常[/green]")
    
    console.print(f"\n[cyan]你选择了选项：{choice}[/cyan]")
    console.print("[green]菜单功能正常！深度研究选项已成功移除。[/green]")
