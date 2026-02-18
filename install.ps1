# Env Tool - One-Command Installer for Windows

Write-Host "🐍 Env Tool Installer" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green

# 1. Check for Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python is not installed. Please install Python 3.7+ first." -ForegroundColor Red
    exit 1
}

# 2. Install via pip
Write-Host "Installing Env Tool from GitHub..." -ForegroundColor Cyan
python -m pip install --upgrade git+https://github.com/AliHamza-Coder/env-tool.git

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Env Tool installed successfully!" -ForegroundColor Green
    Write-Host "Try it out by typing: env" -ForegroundColor Yellow
} else {
    Write-Host "❌ Installation failed. Please check your internet connection and git installation." -ForegroundColor Red
}
