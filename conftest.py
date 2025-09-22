"""
pytest配置文件
"""
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from utils.browser_manager import BrowserManager
from utils.screenshot_helper import ScreenshotHelper
from config.settings import *


@pytest.fixture(scope="session")
def browser_manager():
    """浏览器管理器fixture"""
    manager = BrowserManager()
    manager.start_browser(headless=HEADLESS_MODE, browser_type=BROWSER_TYPE)
    yield manager
    manager.close_browser()


@pytest.fixture(scope="function")
def browser_context(browser_manager):
    """浏览器上下文fixture"""
    context = browser_manager.create_context(
        viewport={'width': BROWSER_WIDTH, 'height': BROWSER_HEIGHT}
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(browser_context):
    """页面fixture"""
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def screenshot_helper(page):
    """截图助手fixture"""
    return ScreenshotHelper(page)


@pytest.fixture(autouse=True)
def test_setup_teardown(page, request):
    """测试设置和清理"""
    # 测试前设置
    page.set_default_timeout(TEST_TIMEOUT)
    
    yield
    
    # 测试后清理
    if SCREENSHOT_ON_FAILURE and request.node.rep_call.failed:
        screenshot_helper = ScreenshotHelper(page)
        test_name = request.node.name
        screenshot_helper.take_screenshot_on_failure(test_name)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """生成测试报告"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session")
def test_data():
    """测试数据fixture"""
    from utils.data_helper import DataHelper
    return DataHelper.load_json("data/test_data.json")


@pytest.fixture(scope="session")
def user_data():
    """用户数据fixture"""
    from utils.data_helper import DataHelper
    return DataHelper.load_yaml("data/users.yaml")


# 参数化fixture
@pytest.fixture(params=["chromium", "firefox", "webkit"])
def browser_type(request):
    """浏览器类型参数化"""
    return request.param


@pytest.fixture(params=["default", "admin", "guest"])
def user_type(request):
    """用户类型参数化"""
    return request.param
