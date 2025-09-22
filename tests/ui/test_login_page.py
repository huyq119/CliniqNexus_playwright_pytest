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
        
        # 验证登录成功后的页面跳转
        # 注意：根据实际网站调整跳转URL
        assert "dashboard" in page.url or "home" in page.url or "success" in page.url
    
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
        
        # 验证错误消息显示
        assert login_page.is_error_message_visible()
    
    @pytest.mark.parametrize("user_type", ["test_env", "default"])
    def test_login_with_different_users(self, page: Page, user_data, user_type):
        """测试不同用户类型的登录"""
        user = user_data.get(user_type)
        if not user:
            pytest.skip(f"用户类型 {user_type} 不存在")
        
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(user['username'], user['password'])
        
        # 验证登录结果（根据实际网站调整）
        # 这里可以根据不同用户类型验证不同的跳转或权限
        assert page.url != login_page.url  # 确保页面发生了变化
