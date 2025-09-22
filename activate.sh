#!/bin/bash
# 激活Python虚拟环境脚本

echo "正在激活Python虚拟环境..."
source venv/bin/activate

echo "虚拟环境已激活！"
echo "Python路径: $(which python)"
echo "Python版本: $(python --version)"
echo ""
echo "可用的测试命令："
echo "  pytest                    # 运行所有测试"
echo "  pytest tests/ui/          # 运行UI测试"
echo "  pytest tests/api/         # 运行API测试"
echo "  pytest tests/e2e/         # 运行端到端测试"
echo "  playwright test           # 运行Playwright测试"
echo ""
echo "要退出虚拟环境，请输入: deactivate"
