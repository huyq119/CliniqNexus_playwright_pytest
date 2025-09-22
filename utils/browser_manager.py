"""
浏览器管理器
"""
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import Optional
import os


class BrowserManager:
    """浏览器管理器类"""
    
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    def start_browser(self, headless: bool = True, browser_type: str = "chromium") -> None:
        """启动浏览器"""
        self.playwright = sync_playwright().start()
        
        if browser_type == "chromium":
            self.browser = self.playwright.chromium.launch(headless=headless)
        elif browser_type == "firefox":
            self.browser = self.playwright.firefox.launch(headless=headless)
        elif browser_type == "webkit":
            self.browser = self.playwright.webkit.launch(headless=headless)
        else:
            raise ValueError(f"不支持的浏览器类型: {browser_type}")
    
    def create_context(self, **kwargs) -> BrowserContext:
        """创建浏览器上下文"""
        if not self.browser:
            raise RuntimeError("浏览器未启动，请先调用 start_browser()")
        
        self.context = self.browser.new_context(**kwargs)
        return self.context
    
    def create_page(self) -> Page:
        """创建新页面"""
        if not self.context:
            self.create_context()
        
        self.page = self.context.new_page()
        return self.page
    
    def close_browser(self) -> None:
        """关闭浏览器"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def take_screenshot(self, name: str, full_page: bool = True) -> str:
        """截图"""
        if not self.page:
            raise RuntimeError("页面未创建")
        
        # 确保截图目录存在
        os.makedirs("screenshots", exist_ok=True)
        
        screenshot_path = f"screenshots/{name}.png"
        self.page.screenshot(path=screenshot_path, full_page=full_page)
        return screenshot_path
