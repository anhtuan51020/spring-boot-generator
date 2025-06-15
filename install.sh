#!/bin/bash

set -e

TOOL_NAME="spring-boot-generator"
VENV_DIR=".venv"
MAIN_MODULE="spring_boot_generator"
BIN_PATH="/usr/local/bin/$TOOL_NAME"
SCRIPT_PATH="$(pwd)/$TOOL_NAME.sh"

echo "🚀 Cài đặt $TOOL_NAME..."

# 1. Tạo virtualenv nếu chưa có
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Tạo môi trường ảo tại $VENV_DIR..."
    python3 -m venv $VENV_DIR
fi

# 2. Kích hoạt virtualenv và cài đặt yêu cầu
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. Tạo file shell runner
echo "🔗 Tạo file shell khởi động CLI: $SCRIPT_PATH"
cat > "$SCRIPT_PATH" <<EOL
#!/bin/bash
source "$(pwd)/$VENV_DIR/bin/activate"
python3 -m $MAIN_MODULE "\$@"
EOL

chmod +x "$SCRIPT_PATH"

# 5. Tạo symlink toàn cục
echo "🔗 Tạo symlink tại $BIN_PATH"
sudo ln -sf "$SCRIPT_PATH" "$BIN_PATH"

echo "✅ Đã cài đặt xong. Bây giờ bạn có thể chạy:"
echo ""
echo "   $ $TOOL_NAME new"
echo ""
