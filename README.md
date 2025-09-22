# CliniqNexus Playwright Pytest 测试框架

这是一个基于 Playwright + pytest 的自动化测试框架，支持 API、UI 和端到端测试。

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/huyq119/CliniqNexus_playwright_pytest.git
cd CliniqNexus_playwright_pytest
```

### 2. 激活虚拟环境

```bash
# 使用激活脚本
./activate.sh

# 或者手动激活
source venv/bin/activate
```

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定类型的测试
pytest tests/ui/          # UI测试
pytest tests/api/         # API测试
pytest tests/e2e/         # 端到端测试

# 运行特定测试文件
pytest tests/ui/test_login_page.py

# 使用Playwright运行测试
playwright test
```

### 3. 查看测试报告

测试报告会生成在 `reports/` 目录下：
- HTML报告：`reports/report.html`
- JSON报告：`reports/report.json`

## 📁 项目结构

```
project/
├── tests/                          # 测试用例
│   ├── api/                        # API测试
│   ├── ui/                         # UI测试
│   └── e2e/                        # 端到端测试
├── pages/                          # 页面对象
│   ├── base_page.py
│   ├── login_page.py
│   └── home_page.py
├── utils/                          # 工具类
│   ├── browser_manager.py
│   ├── data_helper.py
│   └── screenshot_helper.py
├── data/                           # 测试数据
│   ├── test_data.json
│   └── users.yaml
├── config/                         # 配置文件
│   ├── environments.py
│   └── settings.py
├── reports/                        # 测试报告
├── screenshots/                    # 截图存储
├── conftest.py                     # pytest配置
├── pytest.ini                     # pytest设置
├── playwright.config.js            # Playwright配置
├── requirements.txt                # 依赖包
└── activate.sh                     # 虚拟环境激活脚本
```

## 🛠️ 环境配置

### 环境变量

可以通过环境变量来配置测试环境：

```bash
export TEST_ENV=dev          # 测试环境 (dev/staging/production)
export BROWSER_TYPE=chromium # 浏览器类型 (chromium/firefox/webkit)
export HEADLESS=true         # 是否无头模式
```

### 配置文件

- `config/environments.py` - 环境配置管理
- `config/settings.py` - 项目设置配置

## 📊 测试数据

测试数据存储在 `data/` 目录下：

- `test_data.json` - JSON格式的测试数据
- `users.yaml` - YAML格式的用户数据

## 🔧 工具类

### BrowserManager
管理浏览器实例的创建和销毁

### DataHelper
处理测试数据的加载和保存

### ScreenshotHelper
处理测试截图功能

## 📝 编写测试

### 页面对象模式

使用页面对象模式来组织测试代码：

```python
from pages.login_page import LoginPage

def test_login(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("username", "password")
    assert login_page.is_login_successful()
```

### 数据驱动测试

使用参数化测试来运行多组数据：

```python
@pytest.mark.parametrize("username,password", [
    ("user1", "pass1"),
    ("user2", "pass2"),
])
def test_login_with_different_users(page, username, password):
    # 测试逻辑
    pass
```

## 🎯 测试标记

使用pytest标记来分类测试：

```python
@pytest.mark.smoke      # 冒烟测试
@pytest.mark.regression # 回归测试
@pytest.mark.api        # API测试
@pytest.mark.ui         # UI测试
@pytest.mark.e2e        # 端到端测试
```

运行特定标记的测试：

```bash
pytest -m smoke         # 运行冒烟测试
pytest -m "not slow"    # 运行非慢速测试
```

## 📸 截图功能

测试失败时会自动截图，截图保存在 `screenshots/` 目录下。

## 🔍 调试

### 调试模式运行

```bash
# 非无头模式运行（可以看到浏览器）
HEADLESS=false pytest tests/ui/test_login_page.py

# 慢速运行（便于观察）
pytest --slow tests/ui/test_login_page.py
```

### 查看详细输出

```bash
pytest -v -s tests/ui/test_login_page.py
```

## 🚀 CI/CD 集成

项目已配置好CI/CD集成，支持：

- GitHub Actions
- Jenkins
- GitLab CI

## 🌳 分支管理

项目采用 Git Flow 分支策略，确保代码质量和项目稳定性。

### 分支结构

- **`main`** - 生产就绪的稳定代码
- **`develop`** - 集成开发分支
- **`feature/*`** - 功能开发分支
- **`hotfix/*`** - 紧急修复分支
- **`release/*`** - 版本发布分支

### 分支管理工具

使用提供的脚本简化分支操作：

```bash
# 查看分支状态
./scripts/branch_manager.sh status

# 创建功能分支
./scripts/branch_manager.sh create-feature new-feature-name

# 创建热修复分支
./scripts/branch_manager.sh create-hotfix critical-bug

# 创建发布分支
./scripts/branch_manager.sh create-release v1.0.0

# 切换分支
./scripts/branch_manager.sh switch develop

# 同步分支
./scripts/branch_manager.sh sync

# 清理已合并的分支
./scripts/branch_manager.sh cleanup
```

详细的分支策略请参考 [BRANCH_STRATEGY.md](BRANCH_STRATEGY.md)。

## 📚 更多资源

- [Playwright 官方文档](https://playwright.dev/python/)
- [pytest 官方文档](https://docs.pytest.org/)
- [页面对象模式最佳实践](https://playwright.dev/python/docs/pom)
- [Git Flow 工作流程](https://nvie.com/posts/a-successful-git-branching-model/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个测试框架！

## 📄 许可证

MIT License
