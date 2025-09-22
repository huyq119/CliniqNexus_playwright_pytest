#!/usr/bin/env python3
"""
测试环境验证脚本
用于验证测试环境配置是否正确
"""
import os
import sys
import requests
from playwright.sync_api import sync_playwright
from config.environments import EnvironmentConfig
from utils.data_helper import DataHelper


def test_environment_config():
    """测试环境配置"""
    print("🔧 测试环境配置...")
    
    # 测试不同环境配置
    for env in ['dev', 'test', 'staging', 'production']:
        config = EnvironmentConfig(env)
        print(f"  {env}: {config.get_base_url()}")
    
    # 测试当前环境
    current_config = EnvironmentConfig()
    print(f"  当前环境: {current_config.environment}")
    print(f"  当前URL: {current_config.get_base_url()}")
    print("✅ 环境配置测试完成\n")
    return True


def test_network_connectivity():
    """测试网络连接"""
    print("🌐 测试网络连接...")
    
    test_url = "http://62.234.96.153:55409"
    login_url = f"{test_url}/login"
    
    try:
        # 测试基础连接
        response = requests.get(test_url, timeout=10)
        print(f"  基础URL ({test_url}): {response.status_code}")
        
        # 测试登录页面
        response = requests.get(login_url, timeout=10)
        print(f"  登录页面 ({login_url}): {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 网络连接测试通过\n")
            return True
        else:
            print("❌ 网络连接测试失败\n")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络连接错误: {e}\n")
        return False


def test_playwright_navigation():
    """测试Playwright页面导航"""
    print("🎭 测试Playwright页面导航...")
    
    test_url = "http://62.234.96.153:55409/login"
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 设置超时时间
            page.set_default_timeout(10000)
            
            # 导航到登录页面
            page.goto(test_url)
            
            # 获取页面标题
            title = page.title()
            print(f"  页面标题: {title}")
            
            # 获取当前URL
            current_url = page.url
            print(f"  当前URL: {current_url}")
            
            # 检查页面是否加载成功
            if "login" in current_url.lower() or title:
                print("✅ Playwright导航测试通过\n")
                browser.close()
                return True
            else:
                print("❌ Playwright导航测试失败\n")
                browser.close()
                return False
                
    except Exception as e:
        print(f"❌ Playwright测试错误: {e}\n")
        return False


def test_data_configuration():
    """测试数据配置"""
    print("📊 测试数据配置...")
    
    try:
        # 测试用户数据加载
        users_data = DataHelper.load_yaml("data/users.yaml")
        
        # 检查测试环境用户数据
        if 'test_env' in users_data:
            test_user = users_data['test_env']
            print(f"  测试用户: {test_user['username']}")
            print(f"  用户邮箱: {test_user['email']}")
            print("✅ 数据配置测试通过\n")
            return True
        else:
            print("❌ 缺少测试环境用户数据\n")
            return False
            
    except Exception as e:
        print(f"❌ 数据配置错误: {e}\n")
        return False


def main():
    """主函数"""
    print("🚀 开始测试环境验证...\n")
    
    # 设置测试环境
    os.environ['TEST_ENV'] = 'test'
    
    results = []
    
    # 运行各项测试
    results.append(test_environment_config() or 0)
    results.append(test_network_connectivity() or 0)
    results.append(test_playwright_navigation() or 0)
    results.append(test_data_configuration() or 0)
    
    # 汇总结果
    passed = sum(results)
    total = len(results)
    
    print("📋 测试结果汇总:")
    print(f"  通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！环境配置正确。")
        print("\n💡 现在可以运行以下命令开始测试:")
        print("   TEST_ENV=test pytest tests/ui/test_login_page.py -v")
        print("   TEST_ENV=test playwright test")
        return 0
    else:
        print("❌ 部分测试失败，请检查配置。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
