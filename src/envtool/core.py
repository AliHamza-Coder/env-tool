import os
import sys
import subprocess
import venv
import shutil
import requests
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()
ENV_NAME = "myenv"
DEBUG_MODE = False
GITHUB_REPO = "AliHamza-Coder/env-tool"
GLOBAL_ENV_BASE = Path.home() / ".envtool" / "envs"

def set_debug(enabled):
    global DEBUG_MODE
    DEBUG_MODE = enabled

def get_venv_path():
    """Get the path to the virtual environment, checking for local, linked, or common default names."""
    # 1. Check for .envlink (Global Link) - Highest Priority
    link_file = Path.cwd() / ".envlink"
    if link_file.exists():
        try:
            target_path = Path(link_file.read_text().strip())
            if target_path.exists():
                return target_path
        except Exception:
            pass

    # 2. Smart Detection: Search for common venv names
    common_names = [ENV_NAME, ".venv", "venv", "env"]
    for name in common_names:
        local_path = Path.cwd() / name
        # Check if it's a directory and looks like a venv (contains python binary)
        if local_path.is_dir():
            if sys.platform == "win32":
                if (local_path / "Scripts" / "python.exe").exists(): return local_path
            else:
                if (local_path / "bin" / "python").exists(): return local_path
        
    return Path.cwd() / ENV_NAME # Fallback to default name

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
    if not is_online():
        if DEBUG_MODE: console.print("[dim]Offline: Skipping pip upgrade.[/dim]")
        return
        
    python_exe = get_python_exe()
    with console.status("[bold yellow]Upgrading pip...", spinner="dots"):
        run_command([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"])

def install_requirements():
    req_file = Path.cwd() / "requirements.txt"
    if not req_file.exists():
        req_file.touch()
    
    if req_file.stat().st_size > 0:
        if not is_online():
            console.print("[bold red]❌ Offline Mode Detected[/bold red]")
            console.print("[yellow]Please connect to the internet to install dependencies from requirements.txt.[/yellow]")
            return
            
        # UI: Show what's in req.txt first
        with open(req_file, "r") as f:
            lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith("#")]
        
        console.print("\n[bold cyan]📦 Dependency Plan:[/bold cyan]")
        for l in lines[:10]: console.print(f" [dim]•[/dim] {l}")
        if len(lines) > 10: console.print(f" [dim]... and {len(lines)-10} more[/dim]")
        console.print("")

        with console.status("[bold yellow]Installing dependencies...", spinner="dots"):
            pip_exe = get_pip_exe()
            # We run without capture_output to let Pip's progress bars show up if it's an interactive TTY
            # or just to see real-time log.
            run_command([str(pip_exe), "install", "-r", str(req_file)])
        
        console.print("✅ [bold green]Packages installed correctly.[/bold green]")
    else:
        console.print("[yellow]requirements.txt is empty. Skipping install.[/yellow]")

def freeze_dependencies():
    pip_exe = get_pip_exe()
    if not pip_exe.exists():
        return False, "Virtual environment not found. Run 'env' first."
    
    try:
        with console.status("[bold yellow]Freezing dependencies...", spinner="dots"):
            # Preserve comments from existing requirements.txt
            comments = []
            req_file = Path.cwd() / "requirements.txt"
            if req_file.exists():
                with open(req_file, "r") as f:
                    comments = [line for line in f.readlines() if line.strip().startswith("#")]

            result = run_command([str(pip_exe), "freeze"], capture_output=True)
            if result:
                with open("requirements.txt", "w") as f:
                    if comments:
                        f.writelines(comments)
                        f.write("\n")
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
    
    console.print("\n[bold yellow]🔄 Updating Environment Packages...[/bold yellow]")
    console.print("[dim]This will synchronize all packages with requirements.txt and upgrade to latest allowed versions.[/dim]\n")

    with console.status("[bold yellow]Updating...", spinner="dots"):
        result = run_command([str(pip_exe), "install", "--upgrade", "-r", str(req_file)])
        if result:
            return True, "Environment updated successfully."
    return False, "Failed to update dependencies."

def run_in_venv(args):
    python_exe = get_python_exe()
    if not python_exe.exists():
        console.print("[bold red]Venv not detected.[/bold red] Run 'env' to create one first.")
        return
    
    # Load .env variables if present
    load_env()

    # If the command is 'python', replace it with venv python
    if args[0] == "python":
        args[0] = str(python_exe)
    
    run_command(args)

def load_env():
    """Load variables from a .env file into the environment if it exists."""
    env_file = Path.cwd() / ".env"
    if env_file.exists():
        try:
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
            if DEBUG_MODE:
                console.print("[dim]Loaded .env environment variables.[/dim]")
        except Exception as e:
            if DEBUG_MODE: console.print(f"[dim]Failed to load .env: {e}[/dim]")

def clean_project():
    # 1. Handle Global Link (.envlink)
    link_file = Path.cwd() / ".envlink"
    if link_file.exists():
        try:
            link_file.unlink()
            console.print("✅ Removed project link to global environment ([dim].envlink[/dim])")
        except Exception as e:
            console.print(f"[red]Error removing link file:[/red] {e}")

    # 2. Handle Local Venv
    local_venv = Path.cwd() / ENV_NAME
    if local_venv.exists():
        with console.status(f"[bold red]Deleting {ENV_NAME}...", spinner="dots"):
            shutil.rmtree(local_venv)
        console.print(f"✅ Removed local venv [bold]{ENV_NAME}[/bold]")
    else:
        if not link_file.exists():
            console.print("No local environment or link found.")

    # 3. Remove __pycache__
    deleted_caches = 0
    with console.status("[bold red]Cleaning __pycache__ folders...", spinner="dots"):
        for p in Path.cwd().rglob("__pycache__"):
            shutil.rmtree(p)
            deleted_caches += 1
    
    if deleted_caches > 0:
        console.print(f"✅ Removed [bold]{deleted_caches}[/bold] cache directories")
    else:
        console.print("No cache folders found.")

def list_dependencies():
    """List all installed packages in the current context (venv or global)"""
    is_active = is_venv_active()
    context_name = f"Environment: [bold cyan]{ENV_NAME}[/bold cyan]" if is_active else "Environment: [bold yellow]Global (Laptop)[/bold yellow]"
    
    python_exe = get_python_exe() if is_active else sys.executable
    
    with console.status(f"[dim]Fetching packages for {context_name}...", spinner="dots"):
        result = run_command([str(python_exe), "-m", "pip", "list", "--format=json"], capture_output=True)
    
    if not result:
        console.print("[red]Failed to retrieve package list.[/red]")
        return

    import json
    try:
        packages = json.loads(result.stdout)
    except Exception:
        console.print("[red]Error parsing package list.[/red]")
        return

    table = Table(title=f"📦 {context_name}", box=None)
    table.add_column("Package", style="cyan")
    table.add_column("Version", style="green")

    for pkg in packages:
        table.add_row(pkg.get("name"), pkg.get("version"))

    console.print("\n")
    console.print(table)
    console.print("\n")

def is_venv_active():
    """Check if the current process or the calling shell is running inside the project's virtual environment"""
    venv_path = get_venv_path()
    
    # 1. Check the current process prefix
    sys_prefix = Path(sys.prefix).resolve()
    if sys_prefix == venv_path.resolve():
        return True
    
    # 2. Check the shell's VIRTUAL_ENV variable
    shell_venv = os.environ.get("VIRTUAL_ENV")
    if shell_venv:
        return Path(shell_venv).resolve() == venv_path.resolve()
        
    return False

def ensure_requirements_exists():
    """Ensure requirements.txt exists, create it if not."""
    req_file = Path.cwd() / "requirements.txt"
    if not req_file.exists():
        req_file.touch()
        if DEBUG_MODE:
            console.print("[dim]Created missing requirements.txt[/dim]")
    return req_file

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
            f.write("__pycache__/\n*.py[cod]\nmyenv/\n.venv/\nvenv/\nenv/\n.env\n.envlink\n.vscode/\n")
        created.append(".gitignore")
    else:
        # Update existing gitignore with .envlink if missing
        content = gitignore.read_text()
        if ".envlink" not in content:
            with open(gitignore, "a") as f:
                f.write("\n# Env Tool\n.envlink\n")
            created.append(".envlink (added to .gitignore)")
    
    if created:
        console.print(f"✅ Created: [bold]{', '.join(created)}[/bold]")
    else:
        console.print("Project already initialized.")

def is_online(host=None):
    """Robust check if internet is accessible. If a host is provided, it checks specifically for that host."""
    import socket
    
    if host:
        try:
            socket.create_connection((host, 443), timeout=2.0)
            return True
        except (OSError, socket.timeout):
            return False
            
    # General check: try reliable DNS or Web hosts
    checks = [
        ("1.1.1.1", 53),     # Cloudflare DNS
        ("8.8.8.8", 53),     # Google DNS
        ("google.com", 80),  # HTTP
    ]
    
    for h, p in checks:
        try:
            socket.create_connection((h, p), timeout=1.5)
            return True
        except (OSError, socket.timeout):
            continue
    return False

def get_network_diagnostics():
    """Run a comprehensive network check and return detailed status."""
    import socket
    
    # Layer 1: DNS/IP Routing
    dns_ok = False
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=1.5)
        dns_ok = True
    except: pass
    
    # Layer 2: Web Access
    web_ok = False
    try:
        socket.create_connection(("google.com", 80), timeout=1.5)
        web_ok = True
    except: pass
    
    # Layer 3: GitHub API Specific
    github_api_ok = is_online("api.github.com")
    
    return {
        "dns": dns_ok,
        "web": web_ok,
        "github_api": github_api_ok,
        "online": dns_ok or web_ok or github_api_ok
    }

def display_network_status():
    """Check and display a detailed network connectivity breakdown"""
    console.print("\n[bold green]🐍 Env Tool - Network Diagnostics[/bold green]")
    
    with console.status("[dim]Testing connectivity layers...", spinner="dots"):
        diag = get_network_diagnostics()

    # Status Table
    from rich.table import Table
    table = Table(box=None, padding=(0, 2))
    table.add_column("Service", style="cyan")
    table.add_column("Status", justify="right")
    
    table.add_row("Global Internet (DNS)", "[green]ONLINE[/green] ✅" if diag["dns"] else "[red]OFFLINE[/red] ❌")
    table.add_row("Web Services (HTTP)", "[green]ONLINE[/green] ✅" if diag["web"] else "[red]OFFLINE[/red] ❌")
    table.add_row("GitHub API (HTTPS)", "[green]ONLINE[/green] ✅" if diag["github_api"] else "[red]OFFLINE[/red] ❌")
    
    console.print(table)
    
    if diag["github_api"]:
        console.print("\n✨ [bold green]Everything is ready! All services are reachable.[/bold green]\n")
    elif diag["online"]:
        console.print("\n⚠️ [bold yellow]Partial Connectivity Detected.[/bold yellow]")
        console.print("[dim]You are online, but the GitHub API appears unreachable. Check your firewall or proxy.[/dim]\n")
    else:
        console.print("\n❌ [bold red]Offline Mode.[/bold red]")
        console.print("[dim]Please connect to a network to perform upgrades.[/dim]\n")

# --- Global Environment Management ---

def create_global_venv(name):
    """Create a virtual environment in the global central store"""
    if not GLOBAL_ENV_BASE.exists():
        GLOBAL_ENV_BASE.mkdir(parents=True, exist_ok=True)
    
    target_path = GLOBAL_ENV_BASE / name
    if target_path.exists():
        console.print(f"[yellow]Global environment '{name}' already exists.[/yellow]")
        return False
    
    with console.status(f"[bold yellow]Creating global environment: {name}...", spinner="dots"):
        venv.create(target_path, with_pip=True)
    
    console.print(f"✅ Global environment [bold cyan]{name}[/bold cyan] created at {target_path}")
    return True

def list_global_envs():
    """List all centrally stored virtual environments"""
    if not GLOBAL_ENV_BASE.exists() or not any(GLOBAL_ENV_BASE.iterdir()):
        console.print("[dim]No global environments found.[/dim]")
        return
    
    table = Table(title="🌍 [bold green]Global Environments[/bold green]", box=None)
    table.add_column("Name", style="cyan")
    table.add_column("Size", style="dim")
    table.add_column("Path", style="dim")
    
    for venv_dir in GLOBAL_ENV_BASE.iterdir():
        if venv_dir.is_dir():
            # Rough size calculation
            size = sum(f.stat().st_size for f in venv_dir.rglob('*') if f.is_file())
            size_mb = f"{size / (1024 * 1024):.1f} MB"
            table.add_row(venv_dir.name, size_mb, str(venv_dir))
            
    console.print(table)

def link_project_to_global(name):
    """Link the current directory to a global virtual environment"""
    target_path = GLOBAL_ENV_BASE / name
    if not target_path.exists():
        console.print(f"[bold red]Global environment '{name}' does not exist.[/bold red]")
        console.print("Run [bold cyan]env g create " + name + "[/bold cyan] first.")
        return False
    
    link_file = Path.cwd() / ".envlink"
    link_file.write_text(str(target_path.resolve()))
    console.print(f"✅ Project linked to global environment: [bold cyan]{name}[/bold cyan]")
    return True

def remove_global_venv(name=None, remove_all=False):
    """Remove one or all global environments"""
    if not GLOBAL_ENV_BASE.exists():
        return
    
    if remove_all:
        with console.status("[bold red]Deleting all global environments...", spinner="dots"):
            shutil.rmtree(GLOBAL_ENV_BASE)
            GLOBAL_ENV_BASE.mkdir()
        console.print("✅ [bold green]All global environments cleared.[/bold green]")
        return
    
    if name:
        # Path Injection Protection
        if ".." in name or "/" in name or "\\" in name:
            console.print(f"[bold red]Error:[/bold red] Invalid environment name '{name}'.")
            return
            
        target_path = (GLOBAL_ENV_BASE / name).resolve()
        # Verify it's actually within the GLOBAL_ENV_BASE
        if not str(target_path).startswith(str(GLOBAL_ENV_BASE.resolve())):
            console.print(f"[bold red]Error:[/bold red] Security violation. Path outside of global store.")
            return

        if target_path.exists():
            with console.status(f"[bold red]Deleting global env {name}...", spinner="dots"):
                shutil.rmtree(target_path)
            console.print(f"✅ Global environment [bold]{name}[/bold] removed.")
        else:
            console.print(f"[red]Global environment '{name}' not found.[/red]")

def check_latest_version():
    """Fetch the latest version tag from GitHub API"""
    diag = get_network_diagnostics()
    if not diag["github_api"]:
        return "offline" if not diag["online"] else "github_unreachable"
        
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    try:
        headers = {"User-Agent": "EnvTool-CLI-Updater"}
        response = requests.get(url, timeout=5, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("tag_name", "").lstrip("v")
        elif response.status_code == 404:
            return "no_release"
        elif response.status_code == 403:
            return "limit"
        else:
            return f"http_error_{response.status_code}"
    except requests.exceptions.SSLError:
        return "ssl_error"
    except requests.exceptions.Timeout:
        return "timeout"
    except Exception as e:
        if DEBUG_MODE:
            console.print(f"[dim]Version check failed: {e}[/dim]")
        return f"error:{str(e)}"
    return None
