# 🚀 CliniqNexus Playwright 测试框架

基于 Playwright + pytest 的现代化自动化测试框架，支持 API、UI 和端到端测试。

## ⚡ 快速开始

```bash
# 激活环境并运行测试
source activate.sh
python scripts/test_runner.py --login-only
```

## 🎯 主要特性

- ✅ **现代化元素定位**: 优先使用 `get_by_role` 方法
- ✅ **多浏览器支持**: Chromium、Firefox、WebKit
- ✅ **完整 CI/CD**: GitHub Actions 工作流
- ✅ **智能回退机制**: 传统选择器作为备用方案
- ✅ **详细测试报告**: HTML 报告和截图
- ✅ **环境配置管理**: 支持多环境切换

## 🛠️ 常用命令

```bash
# 运行所有测试
python scripts/test_runner.py

# 运行登录测试
python scripts/test_runner.py --login-only

# 调试模式运行
python scripts/test_runner.py --debug --no-headless

# 验证环境配置
python scripts/test_runner.py --validate-env

# 清理旧文件
python scripts/test_runner.py --cleanup
```

## 📁 项目结构

```
├── .github/workflows/          # GitHub Actions 工作流
├── config/                     # 环境配置
├── data/                      # 测试数据
├── pages/                     # 页面对象模型
├── tests/                     # 测试用例
├── utils/                     # 工具类
├── scripts/                   # 脚本文件
│   └── test_runner.py         # 统一测试运行器
├── reports/                   # 测试报告
└── screenshots/               # 测试截图
```

## 🌐 环境配置

```bash
# 测试环境
export TEST_ENV=test
export BASE_URL=http://62.234.96.153:55409
```

## 📚 详细文档

完整文档请查看 [DOCS.md](DOCS.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License