#!/usr/bin/env python3
"""
详细登录测试脚本
用于诊断登录问题
"""
import os
import sys
import time
from playwright.sync_api import sync_playwright
from utils.data_helper import DataHelper


def detailed_login_test():
    """详细的登录测试"""
    print("🔐 开始详细登录测试...")
    
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
            browser = p.chromium.launch(headless=False)  # 显示浏览器
            page = browser.new_page()
            
            # 设置超时时间
            page.set_default_timeout(30000)
            
            print(f"  导航到: {test_url}")
            page.goto(test_url)
            
            # 等待页面加载
            page.wait_for_load_state("networkidle")
            
            # 获取页面标题和URL
            title = page.title()
            current_url = page.url
            print(f"  页面标题: {title}")
            print(f"  当前URL: {current_url}")
            
            # 截图保存当前状态
            page.screenshot(path="screenshots/before_login.png")
            print("  已保存登录前截图: screenshots/before_login.png")
            
            # 查找并填写用户名
            print("  查找用户名输入框...")
            username_selectors = [
                'input[placeholder*="email"]',
                'input[name="username"]',
                'input[name="email"]',
                'input[type="email"]',
                '#username',
                '#email'
            ]
            
            username_input = None
            for selector in username_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        print(f"  找到用户名输入框: {selector}")
                        username_input = element
                        break
                except:
                    continue
            
            if not username_input:
                print("  ❌ 未找到用户名输入框")
                return False
            
            print("  输入用户名...")
            username_input.fill(test_user['username'])
            time.sleep(1)  # 等待输入完成
            
            # 查找并填写密码
            print("  查找密码输入框...")
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                '#password'
            ]
            
            password_input = None
            for selector in password_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        print(f"  找到密码输入框: {selector}")
                        password_input = element
                        break
                except:
                    continue
            
            if not password_input:
                print("  ❌ 未找到密码输入框")
                return False
            
            print("  输入密码...")
            password_input.fill(test_user['password'])
            time.sleep(1)  # 等待输入完成
            
            # 截图保存输入后的状态
            page.screenshot(path="screenshots/after_input.png")
            print("  已保存输入后截图: screenshots/after_input.png")
            
            # 查找并点击登录按钮
            print("  查找登录按钮...")
            login_button_selectors = [
                'button:has-text("Login")',
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("登录")',
                'button:has-text("Sign in")'
            ]
            
            login_button = None
            for selector in login_button_selectors:
                try:
                    element = page.locator(selector).first
                    if element.is_visible():
                        print(f"  找到登录按钮: {selector}")
                        login_button = element
                        break
                except:
                    continue
            
            if not login_button:
                print("  ⚠️  未找到登录按钮，尝试按回车键")
                password_input.press("Enter")
            else:
                print("  点击登录按钮...")
                login_button.click()
            
            # 等待页面响应
            print("  等待页面响应...")
            time.sleep(3)
            
            # 检查是否有错误消息
            print("  检查错误消息...")
            error_selectors = [
                '.error',
                '.alert-danger',
                '.error-message',
                '[class*="error"]',
                '[class*="danger"]',
                '.invalid-feedback',
                '.text-danger'
            ]
            
            has_error = False
            error_text = ""
            for selector in error_selectors:
                try:
                    error_element = page.locator(selector).first
                    if error_element.is_visible():
                        error_text = error_element.text_content()
                        if error_text and error_text.strip():
                            print(f"  ❌ 发现错误消息: {error_text}")
                            has_error = True
                            break
                except:
                    continue
            
            # 截图保存登录后的状态
            page.screenshot(path="screenshots/after_login.png")
            print("  已保存登录后截图: screenshots/after_login.png")
            
            # 检查URL变化
            new_url = page.url
            print(f"  登录后URL: {new_url}")
            
            if has_error:
                print("  ❌ 登录失败，发现错误消息")
                return False
            elif new_url != test_url:
                print("  ✅ 登录成功！页面已跳转")
                return True
            else:
                print("  ⚠️  登录状态不明确，URL未发生变化")
                
                # 检查页面内容是否有变化
                page_content = page.content()
                if "welcome" in page_content.lower() or "dashboard" in page_content.lower():
                    print("  ✅ 页面内容显示登录成功")
                    return True
                else:
                    print("  ❌ 页面内容未显示登录成功迹象")
                    return False
                
    except Exception as e:
        print(f"❌ 测试过程出错: {e}")
        return False
    finally:
        try:
            browser.close()
        except:
            pass


def main():
    """主函数"""
    print("🚀 开始详细登录测试...\n")
    
    success = detailed_login_test()
    
    if success:
        print("\n🎉 登录测试成功！")
        return 0
    else:
        print("\n❌ 登录测试失败")
        print("💡 请检查截图文件以了解详细情况:")
        print("   - screenshots/before_login.png")
        print("   - screenshots/after_input.png") 
        print("   - screenshots/after_login.png")
        return 1


if __name__ == "__main__":
    sys.exit(main())
