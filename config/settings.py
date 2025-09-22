"""
项目设置配置
"""
import os
from config.environments import env_config


# 基础配置
BASE_URL = env_config.get_base_url()
API_BASE_URL = env_config.get_api_url()

# 页面URL配置
LOGIN_URL = f"{BASE_URL}/login"
HOME_URL = f"{BASE_URL}/home"
PROFILE_URL = f"{BASE_URL}/profile"
DASHBOARD_URL = f"{BASE_URL}/dashboard"

# 测试配置
TEST_TIMEOUT = env_config.get_timeout()
HEADLESS_MODE = env_config.is_headless()
DEBUG_MODE = env_config.is_debug()

# 浏览器配置
BROWSER_TYPE = os.getenv('BROWSER_TYPE', 'chromium')
BROWSER_WIDTH = int(os.getenv('BROWSER_WIDTH', '1920'))
BROWSER_HEIGHT = int(os.getenv('BROWSER_HEIGHT', '1080'))

# 截图配置
SCREENSHOT_ON_FAILURE = True
SCREENSHOT_DIR = "screenshots"
SCREENSHOT_RETENTION_DAYS = 7

# 报告配置
REPORT_DIR = "reports"
HTML_REPORT = True
JSON_REPORT = True

# 数据库配置
DATABASE_URL = env_config.get('database_url')

# API配置
API_TIMEOUT = 30
API_RETRY_COUNT = 3

# 用户配置
DEFAULT_USER = {
    'username': 'testuser',
    'password': 'password123',
    'email': 'testuser@example.com'
}

# 日志配置
LOG_LEVEL = 'INFO' if not DEBUG_MODE else 'DEBUG'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 并行测试配置
MAX_WORKERS = int(os.getenv('MAX_WORKERS', '4'))
PARALLEL_TESTS = os.getenv('PARALLEL_TESTS', 'false').lower() == 'true'
