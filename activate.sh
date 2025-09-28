#!/bin/bash
# 简化的环境激活脚本

echo "🚀 激活 CliniqNexus 测试环境..."

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ 虚拟环境已激活"
else
    echo "❌ 虚拟环境不存在，请先创建虚拟环境"
    exit 1
fi

# 设置环境变量
export TEST_ENV=test
export BASE_URL=http://62.234.96.153:55409
export HEADLESS=true
export DEBUG=false

echo "✅ 环境变量已设置"
echo "📋 可用命令:"
echo "  python scripts/test_runner.py --help"
echo "  python scripts/test_runner.py --login-only"
echo "  python scripts/test_runner.py --validate-env"
