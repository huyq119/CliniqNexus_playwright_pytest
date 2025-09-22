# 贡献指南

感谢您对 CliniqNexus Playwright Pytest 测试框架的关注！我们欢迎各种形式的贡献。

## 🚀 快速开始

### 1. Fork 项目

点击项目页面右上角的 "Fork" 按钮，将项目 fork 到您的 GitHub 账户。

### 2. 克隆项目

```bash
git clone https://github.com/您的用户名/CliniqNexus_playwright_pytest.git
cd CliniqNexus_playwright_pytest
```

### 3. 设置开发环境

```bash
# 激活虚拟环境
./activate.sh

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install
```

### 4. 创建功能分支

```bash
git checkout -b feature/your-feature-name
```

## 📝 开发规范

### 代码风格

- 使用 Python 3.9+ 
- 遵循 PEP 8 代码规范
- 使用类型提示 (Type Hints)
- 编写清晰的文档字符串

### 测试规范

- 每个新功能都需要对应的测试用例
- 测试覆盖率应保持在 80% 以上
- 使用描述性的测试名称
- 遵循 AAA 模式 (Arrange, Act, Assert)

### 提交规范

使用清晰的提交信息：

```
feat: 添加新的登录页面测试
fix: 修复浏览器管理器内存泄漏问题
docs: 更新 README 文档
test: 添加用户注册流程测试
refactor: 重构页面对象基类
```

## 🧪 运行测试

```bash
# 运行所有测试
pytest

# 运行特定类型的测试
pytest tests/ui/
pytest tests/api/
pytest tests/e2e/

# 运行特定测试文件
pytest tests/ui/test_login_page.py

# 生成覆盖率报告
pytest --cov=pages --cov=utils --cov-report=html
```

## 📋 提交流程

### 1. 提交更改

```bash
git add .
git commit -m "feat: 添加新的测试功能"
```

### 2. 推送分支

```bash
git push origin feature/your-feature-name
```

### 3. 创建 Pull Request

1. 在 GitHub 上创建 Pull Request
2. 填写详细的描述信息
3. 关联相关的 Issue（如果有）
4. 等待代码审查

## 🐛 报告问题

### Bug 报告

使用 GitHub Issues 报告 bug，请包含：

- 详细的问题描述
- 复现步骤
- 预期行为 vs 实际行为
- 环境信息（Python 版本、操作系统等）
- 相关的日志或截图

### 功能请求

对于新功能请求，请包含：

- 功能描述
- 使用场景
- 预期效果
- 可能的实现方案

## 📚 文档贡献

- 更新 README.md
- 添加代码注释
- 编写使用示例
- 创建教程文档

## 🏷️ 标签说明

- `bug` - 需要修复的问题
- `enhancement` - 功能增强
- `documentation` - 文档相关
- `good first issue` - 适合新手的任务
- `help wanted` - 需要帮助的任务

## 🤝 社区准则

- 保持友善和尊重
- 欢迎不同背景的贡献者
- 提供建设性的反馈
- 帮助其他贡献者

## 📞 联系方式

- GitHub Issues: 用于 bug 报告和功能请求
- GitHub Discussions: 用于一般讨论和问题

## 📄 许可证

本项目采用 MIT 许可证。贡献即表示您同意您的代码将在 MIT 许可证下发布。

---

再次感谢您的贡献！🎉
