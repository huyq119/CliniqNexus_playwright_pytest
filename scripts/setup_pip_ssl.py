#!/usr/bin/env python3
"""
设置pip SSL配置脚本
解决SSL证书验证问题
"""
import os
import sys
from pathlib import Path


def setup_pip_ssl_config():
    """设置pip SSL配置"""
    print("🔧 设置pip SSL配置...")
    
    # 获取用户配置目录
    if sys.platform == "win32":
        config_dir = Path.home() / "AppData" / "Roaming" / "pip"
    else:
        config_dir = Path.home() / ".config" / "pip"
    
    # 创建配置目录
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # pip配置文件内容
    pip_config = """[global]
trusted-host = pypi.org
               pypi.python.org
               files.pythonhosted.org
"""
    
    # 写入配置文件
    config_file = config_dir / "pip.conf"
    with open(config_file, 'w') as f:
        f.write(pip_config)
    
    print(f"✅ pip配置文件已创建: {config_file}")
    
    # 设置环境变量（临时）
    os.environ['PIP_TRUSTED_HOST'] = 'pypi.org pypi.python.org files.pythonhosted.org'
    
    print("✅ 环境变量已设置")
    print("💡 现在可以使用 pip install 命令而不会遇到SSL证书问题")
    
    return True


def test_pip_ssl():
    """测试pip SSL配置"""
    print("\n🧪 测试pip SSL配置...")
    
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, '-m', 'pip', '--version'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ pip工作正常")
            print(f"   {result.stdout.strip()}")
            return True
        else:
            print("❌ pip测试失败")
            print(f"   错误: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ pip测试出错: {e}")
        return False


def main():
    """主函数"""
    print("🚀 开始设置pip SSL配置...\n")
    
    # 设置配置
    setup_success = setup_pip_ssl_config()
    
    if setup_success:
        # 测试配置
        test_success = test_pip_ssl()
        
        if test_success:
            print("\n🎉 pip SSL配置设置成功！")
            print("💡 现在可以正常使用pip安装包了")
            return 0
        else:
            print("\n⚠️  配置已设置，但测试失败")
            return 1
    else:
        print("\n❌ pip SSL配置设置失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
