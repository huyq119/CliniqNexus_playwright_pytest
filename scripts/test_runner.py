#!/usr/bin/env python3
"""
统一测试运行器
整合所有测试功能，提供统一的测试接口
"""
import os
import sys
import argparse
import subprocess
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def setup_environment(env_type='test', headless=True, debug=False):
    """设置测试环境"""
    env = os.environ.copy()
    env['TEST_ENV'] = env_type
    env['HEADLESS'] = str(headless).lower()
    env['DEBUG'] = str(debug).lower()
    env['CI'] = 'true' if os.getenv('CI') else 'false'
    return env

def run_tests(test_file=None, test_function=None, browser='chromium', 
              headless=True, debug=False, generate_report=True):
    """运行测试"""
    print("🧪 开始运行测试...")
    print("=" * 60)
    
    # 设置环境
    env = setup_environment(headless=headless, debug=debug)
    
    # 构建pytest命令
    cmd = [
        'python', '-m', 'pytest',
        '--tb=short',
        '-v'
    ]
    
    # 添加测试文件或函数
    if test_file:
        if test_function:
            cmd.append(f"{test_file}::{test_function}")
        else:
            cmd.append(test_file)
    else:
        cmd.append('tests/')
    
    # 添加浏览器参数
    if browser != 'all':
        cmd.extend(['--browser', browser])
    
    # 添加报告生成
    if generate_report:
        timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"reports/test-report-{timestamp}.html"
        cmd.extend([
            '--html', report_file,
            '--self-contained-html'
        ])
    
    # 调试模式
    if debug:
        cmd.append('-s')  # 显示print输出
    
    try:
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, env=env, cwd=project_root, 
                              capture_output=not debug, text=True)
        
        if not debug:
            print("=" * 60)
            print("测试输出:")
            print(result.stdout)
            
            if result.stderr:
                print("=" * 60)
                print("错误输出:")
                print(result.stderr)
        
        print("=" * 60)
        print(f"测试结果: {'✅ 成功' if result.returncode == 0 else '❌ 失败'}")
        print(f"返回码: {result.returncode}")
        
        if generate_report and result.returncode == 0:
            print(f"📊 测试报告已生成: {report_file}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 运行测试时出错: {e}")
        return False

def run_login_tests(headless=True, debug=False):
    """运行登录相关测试"""
    print("🔐 运行登录测试...")
    return run_tests(
        test_file='tests/ui/test_login_page.py',
        headless=headless,
        debug=debug
    )

def run_element_tests(headless=True, debug=False):
    """运行元素可见性测试"""
    print("👁️ 运行元素可见性测试...")
    return run_tests(
        test_file='tests/ui/test_login_page.py::TestLoginPage::test_login_page_elements',
        headless=headless,
        debug=debug
    )

def run_api_tests():
    """运行API测试"""
    print("🌐 运行API测试...")
    return run_tests(test_file='tests/api/')

def run_e2e_tests():
    """运行端到端测试"""
    print("🔄 运行端到端测试...")
    return run_tests(test_file='tests/e2e/')

def validate_environment():
    """验证环境配置"""
    print("🔍 验证环境配置...")
    
    try:
        from utils.data_helper import DataHelper
        from config.environments import env_config
        
        # 检查用户数据
        users_data = DataHelper.load_yaml("data/users.yaml")
        print(f"✅ 用户数据加载成功，共 {len(users_data)} 个用户")
        
        # 检查环境配置
        base_url = env_config.get_base_url()
        print(f"✅ 环境配置正常，基础URL: {base_url}")
        
        # 检查测试环境用户
        test_user = users_data.get('test_env')
        if test_user:
            print(f"✅ 测试用户配置正常: {test_user.get('username', 'N/A')}")
        else:
            print("⚠️ 未找到测试环境用户配置")
        
        return True
        
    except Exception as e:
        print(f"❌ 环境验证失败: {e}")
        return False

def cleanup_old_files():
    """清理旧文件"""
    print("🧹 清理旧文件...")
    
    # 清理旧截图
    screenshots_dir = project_root / "screenshots"
    if screenshots_dir.exists():
        old_screenshots = list(screenshots_dir.glob("FAILED_*.png"))
        for screenshot in old_screenshots:
            try:
                screenshot.unlink()
                print(f"删除旧截图: {screenshot.name}")
            except Exception as e:
                print(f"删除截图失败 {screenshot.name}: {e}")
    
    # 清理旧报告
    reports_dir = project_root / "reports"
    if reports_dir.exists():
        old_reports = list(reports_dir.glob("*.html"))
        for report in old_reports:
            if report.stat().st_size == 0:  # 删除空文件
                try:
                    report.unlink()
                    print(f"删除空报告: {report.name}")
                except Exception as e:
                    print(f"删除报告失败 {report.name}: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='统一测试运行器')
    parser.add_argument('--test-file', help='指定测试文件')
    parser.add_argument('--test-function', help='指定测试函数')
    parser.add_argument('--browser', choices=['chromium', 'firefox', 'webkit', 'all'], 
                       default='chromium', help='指定浏览器')
    parser.add_argument('--headless', action='store_true', default=True, 
                       help='无头模式运行')
    parser.add_argument('--no-headless', action='store_true', 
                       help='非无头模式运行')
    parser.add_argument('--debug', action='store_true', 
                       help='调试模式')
    parser.add_argument('--no-report', action='store_true', 
                       help='不生成报告')
    parser.add_argument('--validate-env', action='store_true', 
                       help='验证环境配置')
    parser.add_argument('--cleanup', action='store_true', 
                       help='清理旧文件')
    parser.add_argument('--login-only', action='store_true', 
                       help='只运行登录测试')
    parser.add_argument('--elements-only', action='store_true', 
                       help='只运行元素测试')
    parser.add_argument('--api-only', action='store_true', 
                       help='只运行API测试')
    parser.add_argument('--e2e-only', action='store_true', 
                       help='只运行端到端测试')
    
    args = parser.parse_args()
    
    print("🔧 CliniqNexus 测试运行器")
    print("=" * 60)
    
    # 处理无头模式参数
    headless = args.headless and not args.no_headless
    
    # 验证环境
    if args.validate_env:
        if not validate_environment():
            return 1
    
    # 清理旧文件
    if args.cleanup:
        cleanup_old_files()
    
    # 运行特定测试
    success = True
    
    if args.login_only:
        success = run_login_tests(headless=headless, debug=args.debug)
    elif args.elements_only:
        success = run_element_tests(headless=headless, debug=args.debug)
    elif args.api_only:
        success = run_api_tests()
    elif args.e2e_only:
        success = run_e2e_tests()
    else:
        # 运行完整测试
        success = run_tests(
            test_file=args.test_file,
            test_function=args.test_function,
            browser=args.browser,
            headless=headless,
            debug=args.debug,
            generate_report=not args.no_report
        )
    
    print("\n" + "=" * 60)
    print(f"🎯 测试完成: {'✅ 成功' if success else '❌ 失败'}")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

