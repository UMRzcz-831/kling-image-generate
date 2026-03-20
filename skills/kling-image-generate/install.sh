#!/bin/bash
# 可灵图像生成SKILL安装脚本

echo "==================================="
echo "可灵图像生成SKILL安装"
echo "==================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 需要安装Python 3"
    exit 1
fi

# 安装依赖
echo "安装依赖..."
pip3 install -r requirements.txt

# 设置环境变量
echo ""
echo "请设置以下环境变量："
echo ""
echo "export KLING_ACCESS_KEY='your_access_key'"
echo "export KLING_SECRET_KEY='your_secret_key'"
echo ""
echo "可以将上述配置添加到 ~/.bashrc 或 ~/.zshrc 中"
echo ""
echo "安装完成！"
echo ""
echo "使用示例："
echo "  python3 scripts/generate_image.py --prompt '一只可爱的猫咪' --n 2"
