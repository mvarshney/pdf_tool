#!/bin/bash

# PDF Tool Installation Script  
# This script rebuilds and installs the pdf-tool executable

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"

echo "Building PDF Tool executable..."

# Ensure we're in the right directory
cd "$SCRIPT_DIR"

# Clean previous builds
rm -rf dist build

# Build the executable using the spec file
/Users/mvarshne/Documents/work/venv/bin/pyinstaller pdf-tool.spec

# Create install directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Remove old installation
rm -rf "$INSTALL_DIR/pdf-tool-dir"
rm -f "$INSTALL_DIR/pdf-tool"

# Copy the new directory and create wrapper script
cp -r dist/pdf-tool "$INSTALL_DIR/pdf-tool-dir"

# Create wrapper script for convenient access
cat > "$INSTALL_DIR/pdf-tool" << 'EOF'
#!/bin/bash
# PDF Tool wrapper script
exec "$HOME/.local/bin/pdf-tool-dir/pdf-tool" "$@"
EOF

chmod +x "$INSTALL_DIR/pdf-tool"

echo "✅ PDF Tool has been built and installed"
echo "📁 Installation: $INSTALL_DIR/pdf-tool-dir/"
echo "🚀 Command: pdf-tool"

# Test the installation
echo "Testing installation..."
if command -v pdf-tool >/dev/null 2>&1; then
    echo "✅ Installation successful! Use 'pdf-tool' command"
else
    echo "⚠️  pdf-tool is not in PATH. Please ensure $INSTALL_DIR is in your PATH"
    echo "Add this to your ~/.zshrc or ~/.bashrc:"
    echo "export PATH=\"$INSTALL_DIR:\$PATH\""
fi
