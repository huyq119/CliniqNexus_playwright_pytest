# 🚀 CliniqNexus Playwright 测试框架使用指南

## 📋 快速开始

### 1. 环境准备
```bash
# 激活虚拟环境
source activate.sh

# 验证环境配置
PYTHONPATH=. python scripts/test_environment.py
```

### 2. 运行测试

#### 运行所有登录测试
```bash
TEST_ENV=test pytest tests/ui/test_login_page.py -v
```

#### 运行特定测试
```bash
# 测试页面元素
TEST_ENV=test pytest tests/ui/test_login_page.py::TestLoginPage::test_login_page_elements -v

# 测试登录成功
TEST_ENV=test pytest tests/ui/test_login_page.py::TestLoginPage::test_login_success -v

# 测试登录失败
TEST_ENV=test pytest tests/ui/test_login_page.py::TestLoginPage::test_login_failure -v
```

#### 使用Playwright运行测试
```bash
TEST_ENV=test playwright test
```

### 3. 调试和诊断

#### 详细登录测试
```bash
PYTHONPATH=. python scripts/detailed_login_test.py
```

#### 环境验证
```bash
PYTHONPATH=. python scripts/test_environment.py
```

## 🔧 配置说明

### 用户凭据配置
用户凭据已配置在以下文件中：
- `data/users.yaml` - YAML格式
- `data/test_data.json` - JSON格式

当前测试用户：
- **用户名**: `lovely_hu@qq.com`
- **密码**: `test123456`
- **测试网站**: http://62.234.96.153:55409/login

### 环境配置
环境配置在 `config/environments.py` 中：
- `dev` - 开发环境
- `test` - 测试环境 (当前使用)
- `staging` - 预发布环境
- `production` - 生产环境

## 📊 测试报告

### 生成HTML报告
```bash
TEST_ENV=test pytest tests/ui/test_login_page.py --html=reports/report.html --self-contained-html
```

### 生成JSON报告
```bash
TEST_ENV=test pytest tests/ui/test_login_page.py --json-report --json-report-file=reports/report.json
```

## 🎯 测试用例说明

### 登录页面测试 (`tests/ui/test_login_page.py`)

1. **test_login_page_elements** - 验证登录页面元素显示
   - 检查用户名输入框是否可见
   - 检查密码输入框是否可见
   - 检查登录按钮是否可见

2. **test_login_success** - 测试登录成功
   - 使用真实用户凭据登录
   - 验证登录成功指示器
   - 检查无错误消息

3. **test_login_failure** - 测试登录失败
   - 使用无效凭据登录
   - 验证错误消息显示

4. **test_login_with_different_users** - 测试不同用户登录
   - 支持参数化测试
   - 验证不同用户类型的登录

## 🔍 故障排除

### 常见问题

1. **页面元素找不到**
   - 检查页面是否完全加载
   - 验证元素选择器是否正确
   - 使用详细登录测试脚本诊断

2. **登录超时**
   - 检查网络连接
   - 验证网站是否可访问
   - 增加超时时间设置

3. **测试失败**
   - 查看生成的截图文件
   - 检查测试报告
   - 运行环境验证脚本

### 调试工具

1. **截图功能**
   - 自动截图保存在 `screenshots/` 目录
   - 包含登录前、输入后、登录后的截图

2. **详细日志**
   - 使用 `-s` 参数显示详细输出
   - 使用 `-v` 参数显示详细测试信息

3. **环境验证**
   - 运行 `scripts/test_environment.py` 验证配置
   - 运行 `scripts/detailed_login_test.py` 诊断登录问题

## 📁 项目结构

```
CliniqNexus_playwright_pytest/
├── tests/                    # 测试用例
│   ├── ui/                  # UI测试
│   ├── api/                 # API测试
│   └── e2e/                 # 端到端测试
├── pages/                   # 页面对象
├── utils/                   # 工具类
├── data/                    # 测试数据
├── config/                  # 配置文件
├── scripts/                 # 脚本文件
├── reports/                 # 测试报告
└── screenshots/             # 截图文件
```

## 🚀 下一步

1. **扩展测试用例** - 添加更多页面和功能测试
2. **API测试** - 实现API接口测试
3. **端到端测试** - 实现完整的用户流程测试
4. **CI/CD集成** - 配置自动化测试流程

## 📞 支持

如果遇到问题，请：
1. 查看生成的截图和报告
2. 运行环境验证脚本
3. 检查项目文档
4. 提交Issue到GitHub仓库
