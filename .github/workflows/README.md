# GitHub Actions 工作流说明

本目录包含了项目的 GitHub Actions 工作流配置文件，所有工作流都使用了最新的 `actions/upload-artifact@v4` 版本。

## 工作流文件

### 1. ci.yml - 主 CI/CD 流水线
- **触发条件**: 推送到 `main` 或 `develop` 分支，或创建 Pull Request
- **功能**: 
  - 运行 Playwright 测试
  - 代码质量检查（linting）
  - 上传测试结果和报告

### 2. playwright.yml - Playwright 测试专用
- **触发条件**: 推送到 `main` 或 `develop` 分支，或创建 Pull Request
- **功能**:
  - 在多个浏览器中运行测试（Chromium、Firefox、WebKit）
  - 生成详细的测试报告
  - 上传测试结果和截图

### 3. deploy.yml - 部署流水线
- **触发条件**: 推送到 `main` 分支或手动触发
- **功能**:
  - 部署前测试
  - 部署到预发布环境
  - 上传部署相关文件

## 关键特性

### ✅ 使用最新版本
- `actions/upload-artifact@v4` - 最新版本，避免弃用警告
- `actions/checkout@v4` - 最新版本
- `actions/setup-python@v5` - 最新版本

### 📊 测试报告
- HTML 格式的测试报告
- 自动截图上传
- 多浏览器测试支持

### 🔧 配置说明
- Python 3.13 环境
- 自动依赖缓存
- 60分钟超时设置
- 30天文件保留期

## 使用方法

1. 将这些工作流文件推送到您的 GitHub 仓库
2. 工作流将自动在指定条件下触发
3. 在 GitHub Actions 页面查看运行结果
4. 下载测试报告和截图进行分析

## 故障排除

如果遇到 `actions/upload-artifact@v3` 弃用错误：
1. 确保所有工作流文件都使用 `@v4` 版本
2. 检查是否有其他工作流文件使用了旧版本
3. 重新运行工作流

## 自定义配置

您可以根据项目需求修改：
- 测试命令和参数
- 浏览器选择
- 文件保留期
- 触发条件
