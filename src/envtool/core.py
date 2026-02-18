import os
import sys
import subprocess
import venv
from pathlib import Path

ENV_NAME = "myenv"

def get_venv_path():
    return Path.cwd() / ENV_NAME

def get_python_exe():
    venv_path = get_venv_path()
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"

def get_pip_exe():
    venv_path = get_venv_path()
    if sys.platform == "win32":
        return venv_path / "Scripts" / "pip.exe"
    return venv_path / "bin" / "pip"

def create_venv():
    venv_path = get_venv_path()
    if not venv_path.exists():
        print(f"Creating virtual environment in {venv_path}...")
        venv.create(venv_path, with_pip=True)
    return venv_path

def run_command(args, capture_output=False):
    try:
        result = subprocess.run(args, check=True, capture_output=capture_output, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(args)}: {e}")
        return None

def upgrade_pip():
    python_exe = get_python_exe()
    print("Upgrading pip...")
    run_command([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"])

def install_requirements():
    req_file = Path.cwd() / "requirements.txt"
    if not req_file.exists():
        print("Creating requirements.txt...")
        req_file.touch()
    
    if req_file.stat().st_size > 0:
        print("Installing dependencies...")
        pip_exe = get_pip_exe()
        run_command([str(pip_exe), "install", "-r", str(req_file)])
    else:
        print("requirements.txt is empty. Skipping install.")

def freeze_dependencies():
    pip_exe = get_pip_exe()
    if not pip_exe.exists():
        return False, "Virtual environment not found. Run 'env' first."
    
    try:
        result = run_command([str(pip_exe), "freeze"], capture_output=True)
        if result:
            with open("requirements.txt", "w") as f:
                f.write(result.stdout)
            count = len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
            return True, f"Dependencies frozen to requirements.txt ({count} packages)"
    except Exception as e:
        return False, str(e)
    return False, "Failed to freeze dependencies"

def update_dependencies():
    pip_exe = get_pip_exe()
    if not pip_exe.exists():
        return False, "Virtual environment not found. Run 'env' first."
    
    req_file = Path.cwd() / "requirements.txt"
    if not req_file.exists():
        return False, "requirements.txt not found. Run 'env freeze' first."
    
    if req_file.stat().st_size == 0:
        return True, "requirements.txt is empty. Nothing to update."
    
    print("Updating dependencies...")
    result = run_command([str(pip_exe), "install", "--upgrade", "-r", str(req_file)])
    if result:
        return True, "Environment updated successfully."
    return False, "Failed to update dependencies."
