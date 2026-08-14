#!/bin/bash

# For MacOS and Linux systems !!!!!

BINARY_NAME="filenorm"
INSTALL_DIR="/usr/local/bin"

echo "=== Installing $BINARY_NAME ==="

# Detect the correct binary in the current directory
if [ -f "./filenorm-macos-universal" ]; then
    SRC="./filenorm-macos-universal"
elif [ -f "./filenorm-linux-amd64" ]; then
    SRC="./filenorm-linux-amd64"
else
    echo "Error: Compatible binary not found in the current directory!"
    echo "Make sure you are running this script from the folder containing the binary."
    exit 1
fi

# Make the binary executable
chmod +x "$SRC"

# Move the binary to the system PATH (requires sudo privileges)
echo "Moving binary to $INSTALL_DIR (may require your password)..."
if sudo mv "$SRC" "$INSTALL_DIR/$BINARY_NAME"; then
    echo "=== Successfully installed! ==="
    echo "You can now use '$BINARY_NAME' command from anywhere."
else
    echo "Error: Installation failed."
    exit 1
fi