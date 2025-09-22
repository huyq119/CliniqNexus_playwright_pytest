#!/usr/bin/env python3
"""
登录功能测试脚本
用于验证用户凭据是否能够正常登录
"""
import os
import sys
from playwright.sync_api import sync_playwright
from utils.data_helper import DataHelper


def test_login_with_real_credentials():
    """使用真实凭据测试登录功能"""
    print("🔐 测试登录功能...")
    
    # 设置测试环境
    os.environ['TEST_ENV'] = 'test'
    
    # 获取用户数据
    users_data = DataHelper.load_yaml("data/users.yaml")
    test_user = users_data.get('test_env')
    
    if not test_user:
        print("❌ 未找到测试环境用户数据")
        return False
    
    print(f"  用户名: {test_user['username']}")
    print(f"  密码: {'*' * len(test_user['password'])}")
    
    test_url = "http://62.234.96.153:55409/login"
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # 显示浏览器以便观察
            page = browser.new_page()
            
            # 设置超时时间
            page.set_default_timeout(15000)
            
            print(f"  导航到: {test_url}")
            page.goto(test_url)
            
            # 等待页面加载
            page.wait_for_load_state("networkidle")
            
            # 获取页面标题
            title = page.title()
            print(f"  页面标题: {title}")
            
            # 尝试查找登录表单元素
            try:
                # 常见的用户名输入框选择器
                username_selectors = [
                    'input[name="username"]',
                    'input[name="email"]',
                    'input[type="email"]',
                    'input[placeholder*="用户名"]',
                    'input[placeholder*="邮箱"]',
                    'input[placeholder*="username"]',
                    'input[placeholder*="email"]',
                    '#username',
                    '#email',
                    '.username',
                    '.email'
                ]
                
                username_input = None
                for selector in username_selectors:
                    try:
                        username_input = page.locator(selector).first
                        if username_input.is_visible():
                            print(f"  找到用户名输入框: {selector}")
                            break
                    except:
                        continue
                
                if not username_input or not username_input.is_visible():
                    print("  ⚠️  未找到用户名输入框，尝试通用输入框")
                    username_input = page.locator('input[type="text"]').first
                
                # 常见的密码输入框选择器
                password_selectors = [
                    'input[name="password"]',
                    'input[type="password"]',
                    'input[placeholder*="密码"]',
                    'input[placeholder*="password"]',
                    '#password',
                    '.password'
                ]
                
                password_input = None
                for selector in password_selectors:
                    try:
                        password_input = page.locator(selector).first
                        if password_input.is_visible():
                            print(f"  找到密码输入框: {selector}")
                            break
                    except:
                        continue
                
                if not password_input or not password_input.is_visible():
                    print("  ⚠️  未找到密码输入框")
                    return False
                
                # 输入用户名和密码
                print("  输入用户名...")
                username_input.fill(test_user['username'])
                
                print("  输入密码...")
                password_input.fill(test_user['password'])
                
                # 查找登录按钮
                login_button_selectors = [
                    'button[type="submit"]',
                    'input[type="submit"]',
                    'button:has-text("登录")',
                    'button:has-text("Login")',
                    'button:has-text("Sign in")',
                    '.login-button',
                    '.btn-login',
                    '#login',
                    '#submit'
                ]
                
                login_button = None
                for selector in login_button_selectors:
                    try:
                        login_button = page.locator(selector).first
                        if login_button.is_visible():
                            print(f"  找到登录按钮: {selector}")
                            break
                    except:
                        continue
                
                if not login_button or not login_button.is_visible():
                    print("  ⚠️  未找到登录按钮，尝试按回车键")
                    password_input.press("Enter")
                else:
                    print("  点击登录按钮...")
                    login_button.click()
                
                # 等待页面响应
                page.wait_for_timeout(3000)
                
                # 检查登录结果
                current_url = page.url
                print(f"  登录后URL: {current_url}")
                
                # 检查是否有错误消息
                error_selectors = [
                    '.error',
                    '.alert-danger',
                    '.error-message',
                    '[class*="error"]',
                    '[class*="danger"]'
                ]
                
                has_error = False
                for selector in error_selectors:
                    try:
                        error_element = page.locator(selector).first
                        if error_element.is_visible():
                            error_text = error_element.text_content()
                            print(f"  ❌ 登录失败: {error_text}")
                            has_error = True
                            break
                    except:
                        continue
                
                if not has_error:
                    # 检查URL是否发生变化（表示登录成功）
                    if current_url != test_url:
                        print("  ✅ 登录成功！页面已跳转")
                        return True
                    else:
                        print("  ⚠️  登录状态不明确，URL未发生变化")
                        return False
                else:
                    return False
                
            except Exception as e:
                print(f"  ❌ 登录过程出错: {e}")
                return False
            finally:
                browser.close()
                
    except Exception as e:
        print(f"❌ 测试过程出错: {e}")
        return False


def main():
    """主函数"""
    print("🚀 开始登录功能测试...\n")
    
    success = test_login_with_real_credentials()
    
    if success:
        print("\n🎉 登录测试成功！")
        print("💡 现在可以运行完整的测试套件:")
        print("   TEST_ENV=test pytest tests/ui/test_login_page.py -v")
        return 0
    else:
        print("\n❌ 登录测试失败，请检查:")
        print("   1. 网络连接是否正常")
        print("   2. 用户凭据是否正确")
        print("   3. 网站登录页面是否可访问")
        return 1


if __name__ == "__main__":
    sys.exit(main())
