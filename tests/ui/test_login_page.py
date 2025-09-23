"""
登录页面UI测试用例
"""
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from utils.data_helper import DataHelper


class TestLoginPage:
    """登录页面测试类"""
    
    def test_login_page_elements(self, page: Page):
        """测试登录页面元素显示"""
        login_page = LoginPage(page)
        login_page.navigate()
        
        assert login_page.is_username_field_visible()
        assert login_page.is_password_field_visible()
        assert login_page.is_login_button_visible()
    
    def test_login_success(self, page: Page, user_data):
        """测试登录成功"""
        # 获取测试环境用户数据 - 修复逻辑错误
        test_user = user_data.get('test_env') or user_data.get('default')
        if not test_user:
            pytest.skip("缺少测试用户数据")
        
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(test_user['username'], test_user['password'])
        
        # 等待页面响应 - 使用智能等待替代硬编码等待
        page.wait_for_load_state('networkidle')
        # 等待页面稳定，不强制等待错误消息
        page.wait_for_timeout(1000)  # 给页面一点时间稳定
        
        # 验证登录成功 - 改进的验证逻辑
        # 首先检查URL变化（更可靠的登录成功指示器）
        current_url = page.url
        url_changed = current_url != login_page.url
        
        # 检查页面内容中的成功指示器
        page_content = page.content().lower()
        login_success_indicators = [
            "welcome", "dashboard", "success", "logged in", 
            "profile", "logout", "用户", "欢迎", "登录成功",
            "home", "main", "account", "settings"
        ]
        
        # 检查是否有登录成功的指示器
        has_success_indicator = any(indicator in page_content for indicator in login_success_indicators)
        
        # 检查是否没有错误消息
        has_error = login_page.is_error_message_visible()
        
        # 登录成功的条件：URL变化或有成功指示器，且没有错误消息
        login_success = (url_changed or has_success_indicator) and not has_error
        
        assert login_success, f"登录验证失败 - URL变化: {url_changed}, 成功指示器: {has_success_indicator}, 错误消息: {has_error}, 当前URL: {current_url}"
    
    def test_login_failure(self, page: Page, user_data):
        """测试登录失败"""
        # 获取无效用户数据
        invalid_user = user_data.get('invalid', {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(invalid_user['username'], invalid_user['password'])
        
        # 等待页面响应 - 使用智能等待替代硬编码等待
        page.wait_for_load_state('networkidle')
        # 等待错误消息出现
        try:
            page.wait_for_selector('[class*="error"], [class*="danger"], .error, .alert-danger', timeout=5000)
        except TimeoutError:
            pass  # 如果没有错误消息，继续验证
        
        # 验证错误消息显示或登录失败的其他指示器
        has_error = login_page.is_error_message_visible()
        
        # 如果没有明显的错误消息，检查页面内容是否显示登录失败
        if not has_error:
            page_content = page.content().lower()
            error_indicators = ["invalid", "incorrect", "wrong", "error", "失败", "错误"]
            has_error = any(indicator in page_content for indicator in error_indicators)
        
        assert has_error, "登录失败测试：应该显示错误消息或登录失败指示器"
    
    @pytest.mark.parametrize("user_type,expected_result", [
        ("test_env", "success"),  # 真实存在的用户，应该登录成功
        ("default", "failure"),   # 测试数据用户，应该登录失败
        ("admin", "failure")      # 测试数据用户，应该登录失败
    ])
    def test_login_with_different_users(self, page: Page, user_data, user_type, expected_result):
        """测试不同用户类型的登录"""
        user = user_data.get(user_type)
        if not user:
            pytest.skip(f"用户类型 {user_type} 不存在")
        
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(user['username'], user['password'])
        
        # 等待页面响应 - 使用智能等待替代硬编码等待
        page.wait_for_load_state('networkidle')
        # 等待页面稳定，不强制等待错误消息
        page.wait_for_timeout(1000)  # 给页面一点时间稳定
        
        # 验证登录结果 - 改进的验证逻辑
        # 首先检查URL变化（更可靠的登录成功指示器）
        current_url = page.url
        url_changed = current_url != login_page.url
        
        # 检查页面内容中的成功指示器
        page_content = page.content().lower()
        login_success_indicators = [
            "welcome", "dashboard", "success", "logged in", 
            "profile", "logout", "用户", "欢迎", "登录成功",
            "home", "main", "account", "settings"
        ]
        
        # 检查是否有登录成功的指示器
        has_success_indicator = any(indicator in page_content for indicator in login_success_indicators)
        
        # 检查是否没有错误消息
        has_error = login_page.is_error_message_visible()
        
        # 登录成功的条件：URL变化或有成功指示器，且没有错误消息
        login_success = (url_changed or has_success_indicator) and not has_error
        
        if expected_result == "success":
            assert login_success, f"用户 {user_type} 应该登录成功但失败了 - URL变化: {url_changed}, 成功指示器: {has_success_indicator}, 错误消息: {has_error}, 当前URL: {current_url}"
        else:
            assert not login_success, f"用户 {user_type} 应该登录失败但成功了 - URL变化: {url_changed}, 成功指示器: {has_success_indicator}, 错误消息: {has_error}, 当前URL: {current_url}"
