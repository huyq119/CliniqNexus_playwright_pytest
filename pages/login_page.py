"""
登录页面对象
"""
from playwright.sync_api import Page
from .base_page import BasePage
from config.settings import LOGIN_URL


class LoginPage(BasePage):
    """登录页面类"""
    
    # 页面元素选择器 - 基于实际网站结构
    USERNAME_FIELD = 'input[placeholder*="email"]'
    PASSWORD_FIELD = 'input[type="password"]'
    LOGIN_BUTTON = 'button:has-text("Login")'
    ERROR_MESSAGE = '.error, .alert-danger, .error-message, [class*="error"], [class*="danger"]'
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = LOGIN_URL
    
    def navigate(self) -> None:
        """导航到登录页面"""
        super().navigate(self.url)
    
    def is_username_field_visible(self) -> bool:
        """检查用户名输入框是否可见"""
        username_selectors = [
            'input[placeholder*="email"]',
            'input[name="username"]',
            'input[name="email"]',
            'input[type="email"]',
            '#username',
            '#email'
        ]
        
        for selector in username_selectors:
            if self.is_element_visible(selector):
                return True
        return False
    
    def is_password_field_visible(self) -> bool:
        """检查密码输入框是否可见"""
        password_selectors = [
            'input[type="password"]',
            'input[name="password"]',
            '#password'
        ]
        
        for selector in password_selectors:
            if self.is_element_visible(selector):
                return True
        return False
    
    def is_login_button_visible(self) -> bool:
        """检查登录按钮是否可见"""
        login_button_selectors = [
            'button:has-text("Login")',
            'button[type="submit"]',
            'input[type="submit"]',
            'button:has-text("登录")',
            'button:has-text("Sign in")'
        ]
        
        for selector in login_button_selectors:
            if self.is_element_visible(selector):
                return True
        return False
    
    def is_error_message_visible(self) -> bool:
        """检查错误消息是否可见"""
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def login(self, username: str, password: str) -> None:
        """执行登录操作"""
        # 尝试多种用户名输入框选择器
        username_selectors = [
            'input[placeholder*="email"]',
            'input[name="username"]',
            'input[name="email"]',
            'input[type="email"]',
            '#username',
            '#email'
        ]
        
        password_selectors = [
            'input[type="password"]',
            'input[name="password"]',
            '#password'
        ]
        
        login_button_selectors = [
            'button:has-text("Login")',
            'button[type="submit"]',
            'input[type="submit"]',
            'button:has-text("登录")',
            'button:has-text("Sign in")'
        ]
        
        # 查找并填写用户名
        username_filled = False
        for selector in username_selectors:
            try:
                if self.is_element_visible(selector):
                    self.fill_input(selector, username)
                    username_filled = True
                    break
            except:
                continue
        
        if not username_filled:
            raise Exception("无法找到用户名输入框")
        
        # 查找并填写密码
        password_filled = False
        for selector in password_selectors:
            try:
                if self.is_element_visible(selector):
                    self.fill_input(selector, password)
                    password_filled = True
                    break
            except:
                continue
        
        if not password_filled:
            raise Exception("无法找到密码输入框")
        
        # 查找并点击登录按钮
        login_clicked = False
        for selector in login_button_selectors:
            try:
                if self.is_element_visible(selector):
                    self.click_element(selector)
                    login_clicked = True
                    break
            except:
                continue
        
        if not login_clicked:
            # 如果找不到登录按钮，尝试按回车键
            self.page.keyboard.press("Enter")
    
    def get_error_message(self) -> str:
        """获取错误消息文本"""
        return self.get_text(self.ERROR_MESSAGE)
