import os
import sys
import subprocess
import venv
import shutil
import requests
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
ENV_NAME = "myenv"
DEBUG_MODE = False
GITHUB_REPO = "AliHamza-Coder/env-tool"

def set_debug(enabled):
    global DEBUG_MODE
    DEBUG_MODE = enabled

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
        with console.status("[bold yellow]Creating virtual environment...", spinner="dots"):
            venv.create(venv_path, with_pip=True)
    return venv_path

def run_command(args, capture_output=False, shell=False):
    if DEBUG_MODE:
        console.print(f"[dim]Executing: {' '.join(args)}[/dim]")
    
    try:
        result = subprocess.run(
            args, 
            check=True, 
            capture_output=capture_output, 
            text=True, 
            shell=shell
        )
        return result
    except subprocess.CalledProcessError as e:
        if DEBUG_MODE:
            console.print_exception()
        else:
            console.print(f"[bold red]Error:[/bold red] Command '{' '.join(args)}' failed.")
            if e.stderr:
                console.print(f"[red]{e.stderr.strip()}[/red]")
        return None

def upgrade_pip():
    python_exe = get_python_exe()
    with console.status("[bold yellow]Upgrading pip...", spinner="dots"):
        run_command([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"])

def install_requirements():
    req_file = Path.cwd() / "requirements.txt"
    if not req_file.exists():
        req_file.touch()
    
    if req_file.stat().st_size > 0:
        with console.status("[bold yellow]Installing dependencies...", spinner="dots"):
            pip_exe = get_pip_exe()
            run_command([str(pip_exe), "install", "-r", str(req_file)])
    else:
        console.print("[yellow]requirements.txt is empty. Skipping install.[/yellow]")

def freeze_dependencies():
    pip_exe = get_pip_exe()
    if not pip_exe.exists():
        return False, "Virtual environment not found. Run 'env' first."
    
    try:
        with console.status("[bold yellow]Freezing dependencies...", spinner="dots"):
            result = run_command([str(pip_exe), "freeze"], capture_output=True)
            if result:
                with open("requirements.txt", "w") as f:
                    f.write(result.stdout)
                count = len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
                return True, f"Dependencies frozen to requirements.txt ({count} packages)"
    except Exception as e:
        if DEBUG_MODE: console.print_exception()
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
    
    with console.status("[bold yellow]Updating dependencies...", spinner="dots"):
        result = run_command([str(pip_exe), "install", "--upgrade", "-r", str(req_file)])
        if result:
            return True, "Environment updated successfully."
    return False, "Failed to update dependencies."

def run_in_venv(args):
    python_exe = get_python_exe()
    if not python_exe.exists():
        console.print("[bold red]Venv not detected.[/bold red] Run 'env' to create one first.")
        return
    
    # If the command is 'python', replace it with venv python
    if args[0] == "python":
        args[0] = str(python_exe)
    
    run_command(args)

def clean_project():
    # Remove venv
    venv_path = get_venv_path()
    if venv_path.exists():
        with console.status(f"[bold red]Deleting {ENV_NAME}...", spinner="dots"):
            shutil.rmtree(venv_path)
        console.print(f"✅ Removed [bold]{ENV_NAME}[/bold]")

    # Remove __pycache__
    deleted_caches = 0
    with console.status("[bold red]Cleaning __pycache__ folders...", spinner="dots"):
        for p in Path.cwd().rglob("__pycache__"):
            shutil.rmtree(p)
            deleted_caches += 1
    
    if deleted_caches > 0:
        console.print(f"✅ Removed [bold]{deleted_caches}[/bold] cache directories")
    else:
        console.print("No cache folders found.")

def init_project():
    dirs = ["src", "tests", "data"]
    created = []
    
    for d in dirs:
        path = Path.cwd() / d
        if not path.exists():
            path.mkdir()
            created.append(d)
    
    gitignore = Path.cwd() / ".gitignore"
    if not gitignore.exists():
        with open(gitignore, "w") as f:
            f.write("__pycache__/\n*.py[cod]\nmyenv/\n.env\n.vscode/\n")
        created.append(".gitignore")
    
    if created:
        console.print(f"✅ Created: [bold]{', '.join(created)}[/bold]")
    else:
        console.print("Project already initialized.")

def check_latest_version():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    try:
        response = requests.get(url, timeout=3) # Faster timeout for better offline experience
        if response.status_code == 200:
            data = response.json()
            return data.get("tag_name", "").lstrip("v")
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        if DEBUG_MODE:
            console.print("[dim]Offline: Skipping version check.[/dim]")
    except Exception as e:
        if DEBUG_MODE:
            console.print(f"[dim]Version check failed: {e}[/dim]")
    return None
