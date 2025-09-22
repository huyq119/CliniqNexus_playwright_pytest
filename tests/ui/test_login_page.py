"""
登录页面UI测试用例
"""
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage


class TestLoginPage:
    """登录页面测试类"""
    
    def test_login_page_elements(self, page: Page):
        """测试登录页面元素显示"""
        login_page = LoginPage(page)
        login_page.navigate()
        
        assert login_page.is_username_field_visible()
        assert login_page.is_password_field_visible()
        assert login_page.is_login_button_visible()
    
    def test_login_success(self, page: Page):
        """测试登录成功"""
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("testuser", "password123")
        
        # 验证登录成功后的页面跳转
        assert "dashboard" in page.url
    
    def test_login_failure(self, page: Page):
        """测试登录失败"""
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("wronguser", "wrongpassword")
        
        # 验证错误消息显示
        assert login_page.is_error_message_visible()
