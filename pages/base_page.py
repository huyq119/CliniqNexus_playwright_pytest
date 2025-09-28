"""
基础页面类
"""
from playwright.sync_api import Page, expect
from typing import Optional


class BasePage:
    """基础页面类，包含所有页面的通用方法"""
    
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 30000  # 30秒超时
    
    def navigate(self, url: str) -> None:
        """导航到指定URL"""
        try:
            print(f"正在导航到: {url}")
            self.page.goto(url, timeout=60000)  # 增加超时时间到60秒
            print(f"页面加载完成，等待网络空闲...")
            self.page.wait_for_load_state("networkidle", timeout=30000)
            print(f"网络空闲状态达到")
        except Exception as e:
            print(f"导航到 {url} 时出错: {e}")
            # 尝试等待页面加载完成
            try:
                print("尝试等待DOM内容加载...")
                self.page.wait_for_load_state("domcontentloaded", timeout=15000)
                print("DOM内容加载完成")
            except Exception as e2:
                print(f"DOM内容加载也失败: {e2}")
                # 最后尝试等待基本加载状态
                try:
                    self.page.wait_for_load_state("load", timeout=10000)
                    print("基本加载状态达到")
                except Exception as e3:
                    print(f"基本加载状态也失败: {e3}")
                    raise e  # 抛出原始异常
    
    def wait_for_element(self, selector: str, timeout: Optional[int] = None) -> None:
        """等待元素出现"""
        timeout = timeout or self.timeout
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def click_element(self, selector: str) -> None:
        """点击元素"""
        self.page.click(selector)
    
    def fill_input(self, selector: str, text: str) -> None:
        """填充输入框"""
        self.page.fill(selector, text)
    
    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        return self.page.text_content(selector)
    
    def is_element_visible(self, selector: str) -> bool:
        """检查元素是否可见"""
        try:
            # 首先检查页面是否关闭
            if self.page.is_closed():
                print(f"页面已关闭，无法检查元素可见性: {selector}")
                return False
            
            # 检查元素是否存在且可见
            is_visible = self.page.is_visible(selector)
            if is_visible:
                print(f"元素可见: {selector}")
            return is_visible
        except Exception as e:
            print(f"检查元素可见性失败 {selector}: {e}")
            return False
    
    def take_screenshot(self, name: str) -> None:
        """截图"""
        self.page.screenshot(path=f"screenshots/{name}.png")
    
    def wait_for_url(self, url_pattern: str) -> None:
        """等待URL匹配模式"""
        self.page.wait_for_url(url_pattern)
