# 环境配置说明

本文档说明如何配置不同的测试环境。

## 🌐 测试环境配置

### 测试网站地址
- **测试环境URL**: http://62.234.96.153:55409
- **登录页面**: http://62.234.96.153:55409/login

### 环境变量配置

#### 方法1: 环境变量
```bash
# 设置测试环境
export TEST_ENV=test

# 设置基础URL
export BASE_URL=http://62.234.96.153:55409

# 运行测试
pytest tests/ui/test_login_page.py
```

#### 方法2: 命令行参数
```bash
# 使用环境变量运行测试
TEST_ENV=test pytest tests/ui/test_login_page.py

# 使用特定URL运行测试
BASE_URL=http://62.234.96.153:55409 pytest tests/ui/test_login_page.py
```

#### 方法3: 修改配置文件
直接修改 `config/environments.py` 中的默认环境：
```python
self.environment = environment or os.getenv('TEST_ENV', 'test')  # 改为 'test'
```

## 🔧 环境配置详情

### 测试环境 (test)
```python
'test': {
    'base_url': 'http://62.234.96.153:55409',
    'api_url': 'http://62.234.96.153:55409/api',
    'database_url': 'sqlite:///test.db',
    'debug': True,
    'timeout': 30000,
    'headless': False
}
```

### 开发环境 (dev)
```python
'dev': {
    'base_url': 'http://localhost:3000',
    'api_url': 'http://localhost:8000/api',
    'database_url': 'sqlite:///dev.db',
    'debug': True,
    'timeout': 30000,
    'headless': False
}
```

## 🚀 快速开始

### 1. 设置测试环境
```bash
# 激活虚拟环境
./activate.sh

# 设置环境变量
export TEST_ENV=test
```

### 2. 运行登录页面测试
```bash
# 运行UI测试
pytest tests/ui/test_login_page.py -v

# 运行所有UI测试
pytest tests/ui/ -v

# 运行端到端测试
pytest tests/e2e/ -v
```

### 3. 使用Playwright运行测试
```bash
# 设置环境变量后运行
TEST_ENV=test playwright test

# 或者直接指定URL
BASE_URL=http://62.234.96.153:55409 playwright test
```

## 📊 测试数据配置

测试环境的用户数据已配置在 `data/users.yaml` 中：

```yaml
test_env:
  username: "testuser"
  password: "password123"
  email: "testuser@test.com"
  first_name: "测试"
  last_name: "用户"
  role: "user"
```

## 🔍 调试模式

### 启用调试模式
```bash
# 非无头模式运行（可以看到浏览器）
HEADLESS=false pytest tests/ui/test_login_page.py

# 启用详细日志
LOG_LEVEL=DEBUG pytest tests/ui/test_login_page.py
```

### 截图和视频
- 测试失败时会自动截图
- 截图保存在 `screenshots/` 目录
- 视频录制在 `test-results/` 目录

## 🛠️ 故障排除

### 常见问题

1. **连接超时**
   ```bash
   # 增加超时时间
   TEST_TIMEOUT=60000 pytest tests/ui/test_login_page.py
   ```

2. **页面加载失败**
   ```bash
   # 检查网络连接
   curl http://62.234.96.153:55409/login
   ```

3. **元素定位失败**
   ```bash
   # 启用调试模式查看页面
   HEADLESS=false pytest tests/ui/test_login_page.py -s
   ```

### 日志查看
```bash
# 查看详细测试日志
pytest tests/ui/test_login_page.py -v -s --tb=long

# 查看HTML报告
open reports/report.html
```

## 📝 注意事项

1. 确保测试环境服务器可访问
2. 测试数据需要与测试环境匹配
3. 网络环境可能影响测试稳定性
4. 建议在稳定的网络环境下运行测试
