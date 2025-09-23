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
        # 首先验证页面状态
        if self.page.is_closed():
            return False
            
        try:
            # 使用get_by_role方法检查Email输入框
            email_field = self.page.get_by_role("textbox", name="*Email")
            return email_field.is_visible(timeout=3000)
        except (TimeoutError, Exception):
            # 备用方案：使用传统选择器
            username_selectors = [
                'input[placeholder*="email"]',
                'input[name="username"]',
                'input[name="email"]',
                'input[type="email"]',
                '#username',
                '#email'
            ]
            
            for selector in username_selectors:
                try:
                    if self.is_element_visible(selector):
                        return True
                except (TimeoutError, Exception):
                    continue
            return False
    
    def is_password_field_visible(self) -> bool:
        """检查密码输入框是否可见"""
        # 首先验证页面状态
        if self.page.is_closed():
            return False
            
        try:
            # 使用get_by_role方法检查Password输入框
            password_field = self.page.get_by_role("textbox", name="*Password")
            return password_field.is_visible(timeout=3000)
        except (TimeoutError, Exception):
            # 备用方案：使用传统选择器
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                '#password'
            ]
            
            for selector in password_selectors:
                try:
                    if self.is_element_visible(selector):
                        return True
                except (TimeoutError, Exception):
                    continue
            return False
    
    def is_login_button_visible(self) -> bool:
        """检查登录按钮是否可见"""
        # 首先验证页面状态
        if self.page.is_closed():
            return False
            
        try:
            # 使用get_by_role方法检查Login按钮
            login_button = self.page.get_by_role("button", name="Login")
            return login_button.is_visible(timeout=3000)
        except (TimeoutError, Exception):
            # 备用方案：使用传统选择器
            login_button_selectors = [
                'button:has-text("Login")',
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("登录")',
                'button:has-text("Sign in")'
            ]
            
            for selector in login_button_selectors:
                try:
                    if self.is_element_visible(selector):
                        return True
                except (TimeoutError, Exception):
                    continue
            return False
    
    def is_error_message_visible(self) -> bool:
        """检查错误消息是否可见"""
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def login(self, username: str, password: str) -> None:
        """执行登录操作 - 使用get_by_role方法"""
        # 首先验证页面状态
        if self.page.is_closed():
            raise Exception("页面已关闭，无法执行登录操作")
        
        # 等待页面加载完成
        try:
            self.page.wait_for_load_state('domcontentloaded', timeout=10000)
        except Exception as e:
            print(f"页面加载超时: {e}")
        
        try:
            # 使用get_by_role方法进行登录操作
            # 点击并填写Email输入框
            email_field = self.page.get_by_role("textbox", name="*Email")
            email_field.wait_for(state="visible", timeout=5000)
            email_field.click()
            email_field.fill(username)
            
            # 点击并填写Password输入框
            password_field = self.page.get_by_role("textbox", name="*Password")
            password_field.wait_for(state="visible", timeout=5000)
            password_field.click()
            password_field.fill(password)
            
            # 点击Login按钮
            login_button = self.page.get_by_role("button", name="Login")
            login_button.wait_for(state="visible", timeout=5000)
            login_button.click()
            
        except Exception as e:
            # 如果get_by_role方法失败，使用备用方案
            print(f"get_by_role方法失败，使用备用方案: {e}")
            
            # 备用方案：使用传统选择器
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
                except (TimeoutError, Exception):
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
                except (TimeoutError, Exception):
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
                except (TimeoutError, Exception):
                    continue
            
            if not login_clicked:
                # 如果找不到登录按钮，尝试按回车键
                self.page.keyboard.press("Enter")
    
    def get_error_message(self) -> str:
        """获取错误消息文本"""
        return self.get_text(self.ERROR_MESSAGE)
