"""
登录页面对象
"""
from playwright.sync_api import Page
from .base_page import BasePage
from config.settings import LOGIN_URL


class LoginPage(BasePage):
    """登录页面类"""
    
    # 页面元素选择器
    USERNAME_FIELD = "#username"
    PASSWORD_FIELD = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = ".error-message"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = LOGIN_URL
    
    def navigate(self) -> None:
        """导航到登录页面"""
        super().navigate(self.url)
    
    def is_username_field_visible(self) -> bool:
        """检查用户名输入框是否可见"""
        return self.is_element_visible(self.USERNAME_FIELD)
    
    def is_password_field_visible(self) -> bool:
        """检查密码输入框是否可见"""
        return self.is_element_visible(self.PASSWORD_FIELD)
    
    def is_login_button_visible(self) -> bool:
        """检查登录按钮是否可见"""
        return self.is_element_visible(self.LOGIN_BUTTON)
    
    def is_error_message_visible(self) -> bool:
        """检查错误消息是否可见"""
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def login(self, username: str, password: str) -> None:
        """执行登录操作"""
        self.fill_input(self.USERNAME_FIELD, username)
        self.fill_input(self.PASSWORD_FIELD, password)
        self.click_element(self.LOGIN_BUTTON)
    
    def get_error_message(self) -> str:
        """获取错误消息文本"""
        return self.get_text(self.ERROR_MESSAGE)
