基于 Playwright Python 官方文档，我来总结一下如何使用 Playwright 进行 API 测试：

## Playwright API 测试核心概念

### 1. APIRequestContext 基础配置

Playwright 使用 `APIRequestContext` 来发送 HTTP 请求，这是 API 测试的核心组件：

```python
from playwright.sync_api import Playwright, APIRequestContext

def create_api_request_context(playwright: Playwright) -> APIRequestContext:
    return playwright.request.new_context(
        base_url="https://api.example.com",
        extra_http_headers={
            "Authorization": "Bearer token",
            "Content-Type": "application/json"
        }
    )
```

### 2. 基本 HTTP 请求方法

支持所有标准 HTTP 方法：

```python
# GET 请求
response = api_request_context.get("/users/123")

# POST 请求
response = api_request_context.post("/users", data={
    "name": "John Doe",
    "email": "john@example.com"
})

# PUT 请求
response = api_request_context.put("/users/123", data={
    "name": "Jane Doe"
})

# DELETE 请求
response = api_request_context.delete("/users/123")
```

### 3. 响应处理与断言

```python
def test_api_response(api_request_context: APIRequestContext):
    response = api_request_context.get("/users/123")
    
    # 检查状态码
    assert response.status == 200
    
    # 检查响应头
    assert response.headers["content-type"] == "application/json"
    
    # 解析 JSON 响应
    user_data = response.json()
    assert user_data["name"] == "John Doe"
    
    # 获取原始文本
    text_content = response.text()
    
    # 检查响应是否成功
    assert response.ok
```

### 4. 请求参数处理

```python
# 查询参数
response = api_request_context.get("/users", params={
    "page": 1,
    "limit": 10,
    "status": "active"
})

# 表单数据
response = api_request_context.post("/login", form={
    "username": "user",
    "password": "pass"
})

# JSON 数据
response = api_request_context.post("/users", json={
    "name": "John",
    "email": "john@example.com"
})

# 文件上传
response = api_request_context.post("/upload", multipart={
    "file": ("filename.txt", "file content", "text/plain")
})
```

### 5. 身份验证处理

```python
# 使用 Bearer Token
api_request_context = playwright.request.new_context(
    extra_http_headers={
        "Authorization": "Bearer your-token"
    }
)

# 使用 Basic Auth
api_request_context = playwright.request.new_context(
    http_credentials={
        "username": "user",
        "password": "pass"
    }
)
```

### 6. 与 UI 测试集成

```python
def test_ui_with_api_setup(api_request_context: APIRequestContext, page):
    # API 前置条件设置
    api_request_context.post("/test-data/setup")
    
    # UI 测试
    page.goto("https://example.com")
    # ... UI 操作 ...
    
    # API 后置验证
    response = api_request_context.get("/test-data/verify")
    assert response.ok
```

### 7. 状态共享

```python
# 从 API 请求获取认证状态
state = api_request_context.storage_state()

# 在浏览器上下文中使用相同状态
context = browser.new_context(storage_state=state)
page = context.new_page()
```

### 8. 错误处理和重试

```python
# 自动重试配置
api_request_context = playwright.request.new_context(
    timeout=30000,  # 30秒超时
    ignore_https_errors=True  # 忽略 HTTPS 错误
)

# 手动重试逻辑
max_retries = 3
for attempt in range(max_retries):
    try:
        response = api_request_context.get("/api/endpoint")
        if response.ok:
            break
    except Exception as e:
        if attempt == max_retries - 1:
            raise e
        time.sleep(1)
```

### 9. 测试最佳实践

1. **使用 fixture 管理 API 上下文**：
```python
@pytest.fixture
def api_context(playwright):
    context = playwright.request.new_context(
        base_url="https://api.example.com"
    )
    yield context
    context.dispose()
```

2. **数据驱动测试**：
```python
@pytest.mark.parametrize("user_id,expected_name", [
    (1, "John Doe"),
    (2, "Jane Smith"),
])
def test_get_user(api_context, user_id, expected_name):
    response = api_context.get(f"/users/{user_id}")
    assert response.json()["name"] == expected_name
```

3. **环境配置**：
```python
import os

BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com")
API_TOKEN = os.getenv("API_TOKEN")

api_context = playwright.request.new_context(
    base_url=BASE_URL,
    extra_http_headers={"Authorization": f"Bearer {API_TOKEN}"}
)
```

通过这些方法，Playwright 提供了强大而灵活的 API 测试能力，可以与 UI 测试无缝集成，实现端到端的测试覆盖。