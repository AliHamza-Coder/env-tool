#!/bin/bash

# Env Tool - One-Command Installer for Linux/macOS

echo -e "\033[0;32m🐍 Env Tool Installer\033[0m"
echo -e "\033[0;32m======================\033[0m"

# 1. Check for Python
if ! command -v python3 &> /dev/null; then
    echo -e "\033[0;31m❌ python3 is not installed. Please install Python 3.7+ first.\033[0m"
    exit 1
fi

# 2. Install via pip
echo -e "\033[0;36mInstalling Env Tool from GitHub...\033[0m"
python3 -m pip install --upgrade git+https://github.com/AliHamza-Coder/env-tool.git

if [ $? -eq 0 ]; then
    echo -e "\033[0;32m✅ Env Tool installed successfully!\033[0m"
    echo -e "\033[0;33mTry it out by typing: env\033[0m"
else
    echo -e "\033[0;31m❌ Installation failed. Please check your internet connection and git installation.\033[0m"
fi
