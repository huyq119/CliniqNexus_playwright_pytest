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
        """检查用户名输入框是否可见 - 使用get_by_role方法"""
        # 首先验证页面状态
        if self.page.is_closed():
            return False
            
        try:
            # 优先使用get_by_role方法检查Email输入框
            email_field = self.page.get_by_role("textbox", name="*Email")
            if email_field.is_visible(timeout=3000):
                print("使用get_by_role找到Email输入框")
                return True
        except (TimeoutError, Exception) as e:
            print(f"get_by_role方法失败: {e}")
        
        try:
            # 尝试其他可能的role和name组合
            username_field = self.page.get_by_role("textbox", name="*Username")
            if username_field.is_visible(timeout=3000):
                print("使用get_by_role找到Username输入框")
                return True
        except (TimeoutError, Exception) as e:
            print(f"get_by_role Username方法失败: {e}")
        
        try:
            # 尝试通用的textbox role
            textbox_field = self.page.get_by_role("textbox").first
            if textbox_field.is_visible(timeout=3000):
                print("使用get_by_role找到通用textbox")
                return True
        except (TimeoutError, Exception) as e:
            print(f"get_by_role通用textbox方法失败: {e}")
        
        # 备用方案：使用传统选择器
        print("get_by_role方法失败，使用传统选择器作为备用方案")
        username_selectors = [
            'input[placeholder*="email" i]',
            'input[placeholder*="username" i]',
            'input[placeholder*="用户名" i]',
            'input[placeholder*="邮箱" i]',
            'input[name="username"]',
            'input[name="email"]',
            'input[name="user"]',
            'input[name="login"]',
            'input[type="email"]',
            'input[type="text"]',
            '#username',
            '#email',
            '#user',
            '#login',
            'input[class*="username"]',
            'input[class*="email"]',
            'input[class*="user"]',
            'input:not([type="password"]):not([type="submit"]):not([type="button"])'
        ]
        
        for selector in username_selectors:
            try:
                if self.is_element_visible(selector):
                    print(f"使用传统选择器找到用户名输入框: {selector}")
                    return True
            except (TimeoutError, Exception):
                continue
        return False
    
    def is_password_field_visible(self) -> bool:
        """检查密码输入框是否可见 - 使用get_by_role方法"""
        # 首先验证页面状态
        if self.page.is_closed():
            return False
            
        try:
            # 优先使用get_by_role方法检查Password输入框
            password_field = self.page.get_by_role("textbox", name="*Password")
            if password_field.is_visible(timeout=3000):
                print("使用get_by_role找到Password输入框")
                return True
        except (TimeoutError, Exception) as e:
            print(f"get_by_role Password方法失败: {e}")
        
        try:
            # 尝试其他可能的密码相关name
            pass_field = self.page.get_by_role("textbox", name="*Pass")
            if pass_field.is_visible(timeout=3000):
                print("使用get_by_role找到Pass输入框")
                return True
        except (TimeoutError, Exception) as e:
            print(f"get_by_role Pass方法失败: {e}")
        
        try:
            # 尝试通用的password role（如果存在）
            password_role = self.page.get_by_role("password")
            if password_role.is_visible(timeout=3000):
                print("使用get_by_role找到password role")
                return True
        except (TimeoutError, Exception) as e:
            print(f"get_by_role password role方法失败: {e}")
        
        # 备用方案：使用传统选择器
        print("get_by_role方法失败，使用传统选择器作为备用方案")
        password_selectors = [
            'input[type="password"]',
            'input[name="password"]',
            'input[name="pass"]',
            'input[name="pwd"]',
            '#password',
            '#pass',
            '#pwd',
            'input[placeholder*="password" i]',
            'input[placeholder*="密码" i]',
            'input[placeholder*="pass" i]',
            'input[class*="password"]',
            'input[class*="pass"]'
        ]
        
        for selector in password_selectors:
            try:
                if self.is_element_visible(selector):
                    print(f"使用传统选择器找到密码输入框: {selector}")
                    return True
            except (TimeoutError, Exception):
                continue
        return False
    
    def is_login_button_visible(self) -> bool:
        """检查登录按钮是否可见 - 使用get_by_role方法"""
        # 首先验证页面状态
        if self.page.is_closed():
            return False
            
        try:
            # 优先使用get_by_role方法检查Login按钮
            login_button = self.page.get_by_role("button", name="Login")
            if login_button.is_visible(timeout=3000):
                print("使用get_by_role找到Login按钮")
                return True
        except (TimeoutError, Exception) as e:
            print(f"get_by_role Login按钮方法失败: {e}")
        
        try:
            # 尝试其他可能的按钮文本
            signin_button = self.page.get_by_role("button", name="Sign in")
            if signin_button.is_visible(timeout=3000):
                print("使用get_by_role找到Sign in按钮")
                return True
        except (TimeoutError, Exception) as e:
            print(f"get_by_role Sign in按钮方法失败: {e}")
        
        try:
            # 尝试中文登录按钮
            login_cn_button = self.page.get_by_role("button", name="登录")
            if login_cn_button.is_visible(timeout=3000):
                print("使用get_by_role找到中文登录按钮")
                return True
        except (TimeoutError, Exception) as e:
            print(f"get_by_role中文登录按钮方法失败: {e}")
        
        try:
            # 尝试submit按钮
            submit_button = self.page.get_by_role("button", name="Submit")
            if submit_button.is_visible(timeout=3000):
                print("使用get_by_role找到Submit按钮")
                return True
        except (TimeoutError, Exception) as e:
            print(f"get_by_role Submit按钮方法失败: {e}")
        
        try:
            # 尝试通用的button role
            button_role = self.page.get_by_role("button").first
            if button_role.is_visible(timeout=3000):
                print("使用get_by_role找到通用button")
                return True
        except (TimeoutError, Exception) as e:
            print(f"get_by_role通用button方法失败: {e}")
        
        # 备用方案：使用传统选择器
        print("get_by_role方法失败，使用传统选择器作为备用方案")
        login_button_selectors = [
            'button:has-text("Login")',
            'button:has-text("登录")',
            'button:has-text("Sign in")',
            'button:has-text("Sign In")',
            'button:has-text("Log in")',
            'button:has-text("Log In")',
            'input[value*="Login" i]',
            'input[value*="登录" i]',
            'input[value*="Sign in" i]',
            'button[type="submit"]',
            'input[type="submit"]',
            'button[class*="login"]',
            'button[class*="submit"]',
            'input[class*="login"]',
            'input[class*="submit"]',
            '#login',
            '#submit',
            '#login-button',
            '#submit-button',
            'button:not([type="button"])',
            'input[type="submit"]'
        ]
        
        for selector in login_button_selectors:
            try:
                if self.is_element_visible(selector):
                    print(f"使用传统选择器找到登录按钮: {selector}")
                    return True
            except (TimeoutError, Exception):
                continue
        return False
    
    def is_error_message_visible(self) -> bool:
        """检查错误消息是否可见"""
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def login(self, username: str, password: str) -> None:
        """执行登录操作 - 优先使用get_by_role方法"""
        # 首先验证页面状态
        if self.page.is_closed():
            raise Exception("页面已关闭，无法执行登录操作")
        
        # 等待页面加载完成
        try:
            self.page.wait_for_load_state('domcontentloaded', timeout=15000)
        except Exception as e:
            print(f"页面加载超时: {e}")
        
        print("开始使用get_by_role方法进行登录操作...")
        
        # 尝试使用get_by_role方法进行登录
        try:
            # 1. 查找并填写Email输入框
            print("尝试使用get_by_role查找Email输入框...")
            email_field = self.page.get_by_role("textbox", name="*Email")
            email_field.wait_for(state="visible", timeout=5000)
            email_field.click()
            email_field.fill(username)
            print("✅ 使用get_by_role成功填写Email")
            
            # 2. 查找并填写Password输入框
            print("尝试使用get_by_role查找Password输入框...")
            password_field = self.page.get_by_role("textbox", name="*Password")
            password_field.wait_for(state="visible", timeout=5000)
            password_field.click()
            password_field.fill(password)
            print("✅ 使用get_by_role成功填写Password")
            
            # 3. 查找并点击Login按钮
            print("尝试使用get_by_role查找Login按钮...")
            login_button = self.page.get_by_role("button", name="Login")
            login_button.wait_for(state="visible", timeout=5000)
            login_button.click()
            print("✅ 使用get_by_role成功点击Login按钮")
            
            return  # 如果get_by_role方法成功，直接返回
            
        except Exception as e:
            print(f"get_by_role方法失败: {e}")
            print("切换到备用方案：传统选择器方法...")
        
        # 备用方案：使用传统选择器
        username_selectors = [
            'input[placeholder*="email" i]',
            'input[placeholder*="username" i]',
            'input[placeholder*="用户名" i]',
            'input[placeholder*="邮箱" i]',
            'input[name="username"]',
            'input[name="email"]',
            'input[name="user"]',
            'input[name="login"]',
            'input[type="email"]',
            'input[type="text"]',
            '#username',
            '#email',
            '#user',
            '#login',
            'input[class*="username"]',
            'input[class*="email"]',
            'input[class*="user"]',
            'input:not([type="password"]):not([type="submit"]):not([type="button"])'
        ]
        
        password_selectors = [
            'input[type="password"]',
            'input[name="password"]',
            'input[name="pass"]',
            'input[name="pwd"]',
            '#password',
            '#pass',
            '#pwd',
            'input[placeholder*="password" i]',
            'input[placeholder*="密码" i]',
            'input[placeholder*="pass" i]',
            'input[class*="password"]',
            'input[class*="pass"]'
        ]
        
        login_button_selectors = [
            'button:has-text("Login")',
            'button:has-text("登录")',
            'button:has-text("Sign in")',
            'button:has-text("Sign In")',
            'button:has-text("Log in")',
            'button:has-text("Log In")',
            'input[value*="Login" i]',
            'input[value*="登录" i]',
            'input[value*="Sign in" i]',
            'button[type="submit"]',
            'input[type="submit"]',
            'button[class*="login"]',
            'button[class*="submit"]',
            'input[class*="login"]',
            'input[class*="submit"]',
            '#login',
            '#submit',
            '#login-button',
            '#submit-button',
            'button:not([type="button"])',
            'input[type="submit"]'
        ]
        
        # 查找并填写用户名
        username_filled = False
        for selector in username_selectors:
            try:
                if self.is_element_visible(selector):
                    self.fill_input(selector, username)
                    username_filled = True
                    print(f"✅ 使用传统选择器成功填写用户名: {selector}")
                    break
            except (TimeoutError, Exception) as e:
                print(f"❌ 选择器 {selector} 失败: {e}")
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
                    print(f"✅ 使用传统选择器成功填写密码: {selector}")
                    break
            except (TimeoutError, Exception) as e:
                print(f"❌ 密码选择器 {selector} 失败: {e}")
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
                    print(f"✅ 使用传统选择器成功点击登录按钮: {selector}")
                    break
            except (TimeoutError, Exception) as e:
                print(f"❌ 登录按钮选择器 {selector} 失败: {e}")
                continue
        
        if not login_clicked:
            # 如果找不到登录按钮，尝试按回车键
            print("⚠️ 未找到登录按钮，尝试按回车键")
            self.page.keyboard.press("Enter")
    
    def get_error_message(self) -> str:
        """获取错误消息文本"""
        return self.get_text(self.ERROR_MESSAGE)
