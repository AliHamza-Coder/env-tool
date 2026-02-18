import click
import sys
import shutil
from envtool import core, __version__

@click.group(invoke_without_command=True, context_settings=dict(help_option_names=['-h', '--help']))
@click.option("--debug", is_flag=True, help="Show full stack Traces and detailed logs")
@click.pass_context
def main(ctx, debug):
    """🐍 Env Tool - Professional Python Virtual Environment Manager
    
    Developed by Ali Hamza
    """
    core.set_debug(debug)
    
    if ctx.invoked_subcommand is None:
        # Default behavior: Setup environment / Toggle
        core.console.print("\n[bold green]🐍 Env Tool - Context Manager[/bold green]")
        
        # Check if already active
        is_active = core.is_venv_active()
        
        if is_active:
            core.console.print("Status: [bold green]ACTIVE[/bold green]")
            core.console.print(f"You are currently inside the [bold cyan]{core.ENV_NAME}[/bold cyan] environment.")
            core.console.print("\n[bold yellow]To Deactivate, run:[/bold yellow]")
            core.console.print("[bold white]env d[/bold white] (or just type 'deactivate')\n")
            
            if not click.confirm("Do you want to re-run the setup flow anyway?", default=False):
                return
        else:
            core.console.print("Status: [bold yellow]INACTIVE[/bold yellow]")
            core.console.print("Running setup to ensure environment is ready...")

        core.create_venv()
        core.upgrade_pip()
        
        # Ensure req.txt exists and check for dependencies
        req_file = core.ensure_requirements_exists()
        
        if req_file.stat().st_size > 0:
            if click.confirm("\n📦 requirements.txt found. Do you want to install dependencies?", default=True):
                core.install_requirements()
        else:
            core.console.print("[dim]Note: requirements.txt is empty. No dependencies to install.[/dim]")
        
        core.console.print("\n✅ [bold green]Environment Ready.[/bold green]")
        
        # Activation tip if not active
        if not is_active:
            core.console.print("\n[bold yellow]To Activate, run:[/bold yellow]")
            core.console.print("[bold white]env a[/bold white]\n")
    else:
        pass

@main.command()
def list():
    """List all installed packages and their versions"""
    core.list_dependencies()

@main.command()
def net():
    """Check internet connectivity status"""
    core.display_network_status()

@main.command()
@click.pass_context
def help(ctx):
    """Show this help message and exit"""
    click.echo(ctx.parent.get_help())

@main.command()
def a():
    """Activate the virtual environment"""
    venv_path = core.get_venv_path()
    if not venv_path.exists():
        core.console.print("[bold red]Venv not found.[/bold red] Run [bold cyan]env[/bold cyan] first to create it.")
        return

    core.console.print("\n🐍 [bold green]Activation Command:[/bold green]")
    if sys.platform == "win32":
        core.console.print(f"[bold yellow].\\{core.ENV_NAME}\\Scripts\\activate[/bold yellow]\n")
    else:
        core.console.print(f"[bold yellow]source ./{core.ENV_NAME}/bin/activate[/bold yellow]\n")

@main.command()
def d():
    """Deactivate the virtual environment"""
    core.console.print("\n🐍 [bold red]Deactivation Command:[/bold red]")
    core.console.print("[bold yellow]deactivate[/bold yellow]\n")

@main.command()
def help_cmd():
    """Show help message"""
    with click.Context(main) as ctx:
        click.echo(main.get_help(ctx))

@main.command()
def freeze():
    """Export dependencies to requirements.txt"""
    core.console.print("🐍 [bold green]Env Tool - Freeze Dependencies[/bold green]")
    success, message = core.freeze_dependencies()
    if success:
        core.console.print(f"✅ {message}")
    else:
        core.console.print(f"❌ [red]{message}[/red]")

@main.command()
def update():
    """Update all packages to latest versions"""
    core.console.print("🐍 [bold green]Env Tool - Update Environment[/bold green]")
    success, message = core.update_dependencies()
    if success:
        core.console.print(f"✅ {message}")
    else:
        core.console.print(f"[red]{message}[/red]")

@main.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("command", nargs=-1, required=True)
def run(command):
    """Execute a command inside the virtual environment"""
    core.run_in_venv(list(command))

@main.command()
def clean():
    """Reset project by removing venv and cache folders"""
    core.console.print("🐍 [bold red]Env Tool - Clean Project[/bold red]")
    if click.confirm("Are you sure you want to delete the venv and all __pycache__ folders?"):
        core.clean_project()
        core.console.print("✨ [bold green]Project cleaned.[/bold green]")
    else:
        core.console.print("Clean cancelled.")

@main.command()
def init():
    """Bootstrap project with src, tests, and .gitignore"""
    core.console.print("🐍 [bold green]Env Tool - Project Init[/bold green]")
    core.init_project()

@main.command()
def version():
    """Show Env Tool and Python version info"""
    core.console.print("🐍 [bold green]Env Tool - Version Information[/bold green]")
    core.console.print(f"Current Env Tool Version: [bold cyan]{__version__}[/bold cyan]")
    
    # Check for updates
    with core.console.status("[dim]Checking for updates...", spinner="dots"):
        latest = core.check_latest_version()
    
    if latest and latest != __version__:
        core.console.print(f"\n[bold yellow]🔔 A new version is available: {latest}[/bold yellow]")
        core.console.print(f"Run [bold cyan]env upgrade[/bold cyan] to update instantly.\n")
    elif latest == __version__:
        core.console.print("[dim](You are on the latest version)[/dim]\n")
    else:
        # If latest is None, it could be offline or a server error
        if not core.is_online():
            core.console.print("[dim](Version check skipped: Offline)[/dim]\n")
        else:
            core.console.print("[dim](Could not reach GitHub for updates)[/dim]\n")

    python_ver = core.run_command([sys.executable, "--version"], capture_output=True)
    if python_ver:
        core.console.print(f"Global Python version: {python_ver.stdout.strip()}")
    
    env_python = core.get_python_exe()
    if env_python.exists():
        env_ver = core.run_command([str(env_python), "--version"], capture_output=True)
        if env_ver:
            core.console.print(f"Environment Python version: {env_ver.stdout.strip()}")

@main.command()
def upgrade():
    """Update Env Tool to latest version"""
    core.console.print("🐍 [bold green]Env Tool - Upgrade[/bold green]")
    
    with core.console.status("[dim]Checking for updates...", spinner="dots"):
        latest = core.check_latest_version()
    
    if not latest:
        core.console.print("[bold red]❌ Network Error[/bold red]")
        core.console.print("[yellow]Please connect to the internet to check for updates and upgrade Env Tool.[/yellow]")
        if not click.confirm("\nAttempt force-upgrade anyway?"):
            return
    elif latest == __version__:
        core.console.print(f"[green]You are already on the latest version ({__version__}).[/green]")
        if not click.confirm("Do you want to reinstall/force-update anyway?"):
            return
    else:
        core.console.print(f"\n[bold blue]Update Found![/bold blue]")
        core.console.print(f"Current Version: [bold red]{__version__}[/bold red]")
        core.console.print(f"Latest Version:  [bold green]{latest}[/bold green]\n")
        if not click.confirm("Proceed with upgrade?"):
            return

    core.console.print("Updating via pip...")
    core.run_command([sys.executable, "-m", "pip", "install", "--upgrade", "env-tool"])
    core.console.print("✅ [bold green]Upgrade command executed. Please restart your terminal to see changes.[/bold green]")

@main.command()
def uninstall():
    """Completely remove Env Tool from system"""
    core.console.print("🐍 [bold red]Env Tool - Uninstaller[/bold red]", style="bold red")
    
    # Try to find where the 'env' command is located
    env_binary = shutil.which("env")
    
    if click.confirm("\n⚠️ This will remove Env Tool and all its shortcuts. Proceed?"):
        core.console.print("Uninstalling package via pip...", style="dim")
        core.run_command([sys.executable, "-m", "pip", "uninstall", "env-tool", "-y"])
        
        # Manual cleanup for common Windows leftovers
        if sys.platform == "win32" and env_binary:
            binary_path = core.Path(env_binary)
            scripts_dir = binary_path.parent
            
            # Common patterns for pip-installed entry points on Windows
            patterns = ["env.exe", "env-script.py", "env.cmd", "env.ps1"]
            cleaned = []
            
            for p in patterns:
                file_to_del = scripts_dir / p
                if file_to_del.exists():
                    try:
                        file_to_del.unlink()
                        cleaned.append(p)
                    except Exception:
                        pass # Likely in use or already gone
            
            if cleaned:
                core.console.print(f"🧹 Cleaned leftovers: [dim]{', '.join(cleaned)}[/dim]")

        core.console.print("\n✅ [bold green]Env Tool has been thoroughly uninstalled.[/bold green]")
        core.console.print("[yellow]Note: You may need to restart your terminal for all changes to take effect.[/yellow]")
    else:
        core.console.print("Uninstall cancelled.")

if __name__ == "__main__":
    main()
