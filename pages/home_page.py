"""
首页页面对象
"""
from playwright.sync_api import Page
from .base_page import BasePage
from config.settings import HOME_URL


class HomePage(BasePage):
    """首页页面类"""
    
    # 页面元素选择器
    USER_AVATAR = ".user-avatar"
    PROFILE_LINK = "#profile-link"
    LOGOUT_BUTTON = "#logout-button"
    WELCOME_MESSAGE = ".welcome-message"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = HOME_URL
    
    def navigate(self) -> None:
        """导航到首页"""
        super().navigate(self.url)
    
    def is_user_logged_in(self) -> bool:
        """检查用户是否已登录"""
        return self.is_element_visible(self.USER_AVATAR)
    
    def navigate_to_profile(self) -> None:
        """导航到用户资料页面"""
        self.click_element(self.PROFILE_LINK)
        self.wait_for_url("**/profile")
    
    def logout(self) -> None:
        """执行登出操作"""
        self.click_element(self.LOGOUT_BUTTON)
        self.wait_for_url("**/login")
    
    def get_welcome_message(self) -> str:
        """获取欢迎消息"""
        return self.get_text(self.WELCOME_MESSAGE)
