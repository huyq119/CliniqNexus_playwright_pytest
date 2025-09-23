#!/bin/bash

# 测试运行脚本
# 自动设置正确的测试环境

echo "🚀 启动CliniqNexus测试..."

# 激活虚拟环境
source venv/bin/activate

# 设置测试环境
export TEST_ENV=test

echo "📋 环境配置:"
echo "  - 测试环境: $TEST_ENV"
echo "  - 基础URL: http://62.234.96.153:55409"
echo "  - 测试用户: lovely_hu@qq.com"
echo ""

# 检查参数
if [ $# -eq 0 ]; then
    echo "🔍 运行所有登录测试..."
    pytest -v tests/ui/test_login_page.py
elif [ "$1" = "elements" ]; then
    echo "🔍 运行页面元素测试..."
    pytest -v -s tests/ui/test_login_page.py::TestLoginPage::test_login_page_elements
elif [ "$1" = "success" ]; then
    echo "🔍 运行登录成功测试..."
    pytest -v -s tests/ui/test_login_page.py::TestLoginPage::test_login_success
elif [ "$1" = "failure" ]; then
    echo "🔍 运行登录失败测试..."
    pytest -v -s tests/ui/test_login_page.py::TestLoginPage::test_login_failure
elif [ "$1" = "all" ]; then
    echo "🔍 运行所有登录测试..."
    pytest -v -s tests/ui/test_login_page.py
elif [ "$1" = "ui" ]; then
    echo "🔍 运行所有UI测试..."
    pytest -v -s tests/ui/
elif [ "$1" = "api" ]; then
    echo "🔍 运行所有API测试..."
    pytest -v -s tests/api/
elif [ "$1" = "e2e" ]; then
    echo "🔍 运行所有端到端测试..."
    pytest -v -s tests/e2e/
else
    echo "🔍 运行自定义测试: $*"
    pytest -v -s "$@"
fi

echo ""
echo "✅ 测试完成！"
