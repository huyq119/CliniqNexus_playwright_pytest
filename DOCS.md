# 📚 CliniqNexus Playwright 测试框架文档

## 🎯 项目概述

这是一个基于 Playwright + pytest 的自动化测试框架，支持 API、UI 和端到端测试。项目使用 Python 和 Playwright 进行浏览器自动化，pytest 作为测试运行器。

## 🚀 快速开始

### 环境准备

```bash
# 激活虚拟环境
source activate.sh
# 或手动激活
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install --with-deps
```

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行 UI 测试
pytest tests/ui/ -v

# 运行特定测试
pytest tests/ui/test_login_page.py::TestLoginPage::test_login_page_elements -v

# 生成 HTML 报告
pytest tests/ --html=reports/report.html --self-contained-html
```

## 🌐 环境配置

### 测试环境

- **测试环境URL**: http://62.234.96.153:55409
- **登录页面**: http://62.234.96.153:55409/login

### 环境变量

```bash
# 设置测试环境
export TEST_ENV=test

# 设置基础URL
export BASE_URL=http://62.234.96.153:55409

# 设置无头模式
export HEADLESS=true

# 设置调试模式
export DEBUG=true
```

## 🔧 项目结构

```
CliniqNexus_playwright_pytest/
├── .github/workflows/          # GitHub Actions 工作流
├── config/                     # 配置文件
│   ├── environments.py        # 环境配置
│   └── settings.py            # 项目设置
├── data/                      # 测试数据
│   ├── test_data.json        # 测试数据
│   └── users.yaml            # 用户数据
├── pages/                     # 页面对象模型
│   ├── base_page.py          # 基础页面类
│   ├── login_page.py         # 登录页面
│   └── home_page.py          # 首页
├── tests/                     # 测试用例
│   ├── api/                  # API 测试
│   ├── ui/                   # UI 测试
│   └── e2e/                  # 端到端测试
├── utils/                     # 工具类
│   ├── browser_manager.py    # 浏览器管理
│   ├── data_helper.py        # 数据助手
│   └── screenshot_helper.py  # 截图助手
├── scripts/                   # 脚本文件
│   ├── test_runner.py        # 测试运行器
│   └── setup_pip_ssl.py      # SSL 配置
├── reports/                   # 测试报告
├── screenshots/               # 测试截图
└── docs/                      # 文档
```

## 🎨 页面对象模型

### 登录页面 (LoginPage)

使用 `get_by_role` 方法进行元素定位，提供更好的可维护性和稳定性：

```python
# 优先使用 get_by_role 方法
email_field = self.page.get_by_role("textbox", name="*Email")
password_field = self.page.get_by_role("textbox", name="*Password")
login_button = self.page.get_by_role("button", name="Login")

# 备用方案：传统选择器
username_selectors = [
    'input[placeholder*="email" i]',
    'input[name="username"]',
    'input[type="email"]',
    # ... 更多选择器
]
```

### 基础页面 (BasePage)

提供通用的页面操作方法：

- `navigate(url)` - 导航到指定URL
- `click_element(selector)` - 点击元素
- `fill_input(selector, text)` - 填充输入框
- `is_element_visible(selector)` - 检查元素可见性
- `take_screenshot(name)` - 截图

## 🧪 测试用例

### UI 测试

```python
def test_login_success(self, page: Page, user_data):
    """测试登录成功"""
    test_user = user_data.get('test_env')
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(test_user['username'], test_user['password'])
    
    # 验证登录成功
    assert not login_page.is_error_message_visible()
```

### 参数化测试

```python
@pytest.mark.parametrize("user_type,expected_result", [
    ("test_env", "success"),
    ("default", "failure"),
    ("admin", "failure")
])
def test_login_with_different_users(self, page: Page, user_data, user_type, expected_result):
    """测试不同用户类型的登录"""
    user = user_data.get(user_type)
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(user['username'], user['password'])
```

## 🔒 SSL 证书问题解决

如果遇到 SSL 证书验证错误，运行以下脚本：

```bash
python scripts/setup_pip_ssl.py
```

## 🚀 CI/CD 集成

项目包含完整的 GitHub Actions 工作流：

- **ci.yml** - 主 CI/CD 流水线
- **playwright.yml** - Playwright 测试专用
- **deploy.yml** - 部署流水线
- **debug.yml** - 调试工作流

所有工作流都使用最新版本的 `actions/upload-artifact@v4`。

## 🛠️ 开发工具

### 测试运行器

```bash
# 运行所有测试
python scripts/test_runner.py

# 运行特定测试
python scripts/test_runner.py --test-file tests/ui/test_login_page.py

# 运行调试模式
python scripts/test_runner.py --debug
```

### 环境验证

```bash
# 验证环境配置
python scripts/test_environment.py
```

## 📊 测试报告

测试运行后会生成：

- **HTML 报告**: `reports/report.html`
- **截图**: `screenshots/` 目录
- **日志**: 控制台输出

## 🔧 故障排除

### 常见问题

1. **页面元素定位失败**
   - 检查页面是否完全加载
   - 验证元素选择器是否正确
   - 查看控制台日志获取详细信息

2. **浏览器连接问题**
   - 检查网络连接
   - 验证目标网站是否可访问
   - 尝试增加超时时间

3. **测试数据问题**
   - 检查 `data/users.yaml` 文件
   - 验证用户凭据是否有效
   - 确认测试环境配置

### 调试技巧

```bash
# 启用详细日志
export DEBUG=true

# 非无头模式运行
export HEADLESS=false

# 增加超时时间
export TEST_TIMEOUT=60000
```

## 📝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。

## 🤝 支持

如有问题，请：

1. 查看本文档
2. 检查 GitHub Issues
3. 创建新的 Issue

---

**最后更新**: 2024年12月

