# 开发工具目录

本目录包含开发过程中使用的辅助工具和脚本。

## 📁 文件说明

### quick_test.py
快速测试脚本，用于快速验证 Web Search 功能。

**运行方式：**
```bash
python tools/quick_test.py
```

**功能：**
- 执行简单的搜索测试
- 验证基本功能是否正常
- 快速反馈结果

### test_menu.py
测试菜单程序，提供交互式测试界面。

**运行方式：**
```bash
python tools/test_menu.py
```

**功能：**
- 交互式测试菜单
- 支持多种测试场景
- 便于开发调试

## 🎯 使用场景

这些工具主要用于：

1. **开发调试**：快速验证功能
2. **问题排查**：隔离测试特定功能
3. **性能测试**：测试不同搜索模式
4. **示例参考**：了解如何使用 API

## 📚 相关文档

- [测试指南](../docs/development/testing.md)
- [API 参考文档](../docs/guides/api-reference.md)
- [开发环境搭建](../docs/development/setup.md)

## 🔍 与 tests/ 的区别

- **`tools/`**：开发辅助工具，用于手动测试和调试
- **`tests/`**：自动化单元测试，用于持续集成

---

**需要帮助？** 查看 [完整文档](../docs/)
