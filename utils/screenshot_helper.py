"""
截图助手工具类
"""
import os
import time
from datetime import datetime
from playwright.sync_api import Page
from typing import Optional


class ScreenshotHelper:
    """截图助手类"""
    
    def __init__(self, page: Page):
        self.page = page
        self.screenshot_dir = "screenshots"
        self._ensure_screenshot_dir()
    
    def _ensure_screenshot_dir(self) -> None:
        """确保截图目录存在"""
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def take_screenshot(self, name: str, full_page: bool = True) -> str:
        """截图"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        self.page.screenshot(path=filepath, full_page=full_page)
        return filepath
    
    def take_element_screenshot(self, selector: str, name: str) -> str:
        """对特定元素截图"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        element = self.page.locator(selector)
        element.screenshot(path=filepath)
        return filepath
    
    def take_screenshot_on_failure(self, test_name: str) -> str:
        """测试失败时截图"""
        return self.take_screenshot(f"FAILED_{test_name}")
    
    def take_screenshot_on_success(self, test_name: str) -> str:
        """测试成功时截图"""
        return self.take_screenshot(f"SUCCESS_{test_name}")
    
    def cleanup_old_screenshots(self, days: int = 7) -> None:
        """清理旧截图"""
        current_time = time.time()
        cutoff_time = current_time - (days * 24 * 60 * 60)
        
        for filename in os.listdir(self.screenshot_dir):
            filepath = os.path.join(self.screenshot_dir, filename)
            if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff_time:
                os.remove(filepath)
                print(f"已删除旧截图: {filename}")
