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
        # 获取测试环境用户数据
        test_user = user_data.get('test_env', user_data.get('default'))
        
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(test_user['username'], test_user['password'])
        
        # 等待页面响应
        page.wait_for_timeout(3000)
        
        # 验证登录成功 - 检查页面内容而不是URL变化
        page_content = page.content().lower()
        login_success_indicators = [
            "welcome", "dashboard", "success", "logged in", 
            "profile", "logout", "用户", "欢迎", "登录成功"
        ]
        
        # 检查是否有登录成功的指示器
        has_success_indicator = any(indicator in page_content for indicator in login_success_indicators)
        
        # 检查是否没有错误消息
        has_error = login_page.is_error_message_visible()
        
        # 登录成功的条件：有成功指示器且没有错误消息
        assert has_success_indicator and not has_error, f"登录验证失败 - 成功指示器: {has_success_indicator}, 错误消息: {has_error}"
    
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
        
        # 等待页面响应
        page.wait_for_timeout(3000)
        
        # 验证错误消息显示或登录失败的其他指示器
        has_error = login_page.is_error_message_visible()
        
        # 如果没有明显的错误消息，检查页面内容是否显示登录失败
        if not has_error:
            page_content = page.content().lower()
            error_indicators = ["invalid", "incorrect", "wrong", "error", "失败", "错误"]
            has_error = any(indicator in page_content for indicator in error_indicators)
        
        assert has_error, "登录失败测试：应该显示错误消息或登录失败指示器"
    
    @pytest.mark.parametrize("user_type", ["test_env"])
    def test_login_with_different_users(self, page: Page, user_data, user_type):
        """测试不同用户类型的登录"""
        user = user_data.get(user_type)
        if not user:
            pytest.skip(f"用户类型 {user_type} 不存在")
        
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(user['username'], user['password'])
        
        # 等待页面响应
        page.wait_for_timeout(3000)
        
        # 验证登录结果 - 检查页面内容而不是URL变化
        page_content = page.content().lower()
        login_success_indicators = [
            "welcome", "dashboard", "success", "logged in", 
            "profile", "logout", "用户", "欢迎", "登录成功"
        ]
        
        # 检查是否有登录成功的指示器
        has_success_indicator = any(indicator in page_content for indicator in login_success_indicators)
        
        # 检查是否没有错误消息
        has_error = login_page.is_error_message_visible()
        
        # 登录成功的条件：有成功指示器且没有错误消息
        assert has_success_indicator and not has_error, f"用户 {user_type} 登录验证失败 - 成功指示器: {has_success_indicator}, 错误消息: {has_error}"
