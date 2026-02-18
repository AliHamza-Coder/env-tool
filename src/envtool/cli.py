import click
import sys
from envtool import core, __version__

@click.group(invoke_without_command=True)
@click.option("--debug", is_flag=True, help="Show full stack Traces and detailed logs")
@click.pass_context
def main(ctx, debug):
    """🐍 Env Tool - Professional Python Virtual Environment Manager"""
    core.set_debug(debug)
    
    if ctx.invoked_subcommand is None:
        # Default behavior: Setup environment
        core.console.print("\n[bold green]🐍 Env Tool - Setting up Environment[/bold green]")
        core.create_venv()
        core.upgrade_pip()
        
        # Dependency confirmation
        req_file = core.Path.cwd() / "requirements.txt"
        if req_file.exists() and req_file.stat().st_size > 0:
            if click.confirm("\n📦 requirements.txt found. Do you want to install dependencies?"):
                core.install_requirements()
        
        core.console.print("\n✅ [bold green]Environment Ready and Active.[/bold green]\n")
        
        # Activation tip
        if sys.platform == "win32":
            core.console.print("Tip: To activate, run: [bold yellow]env a[/bold yellow]")
        else:
            core.console.print("Tip: To activate, run: [bold yellow]env a[/bold yellow]")
    else:
        pass

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
        core.console.print(f"Run [bold cyan]env self-update[/bold cyan] to upgrade.\n")
    elif latest == __version__:
        core.console.print("[dim](You are on the latest version)[/dim]\n")

    python_ver = core.run_command([sys.executable, "--version"], capture_output=True)
    if python_ver:
        core.console.print(f"Global Python version: {python_ver.stdout.strip()}")
    
    env_python = core.get_python_exe()
    if env_python.exists():
        env_ver = core.run_command([str(env_python), "--version"], capture_output=True)
        if env_ver:
            core.console.print(f"Environment Python version: {env_ver.stdout.strip()}")

@main.command()
def self_update():
    """Update Env Tool to latest version"""
    core.console.print("🐍 [bold green]Env Tool - Self Update[/bold green]")
    core.console.print("Updating via pip...")
    core.run_command([sys.executable, "-m", "pip", "install", "--upgrade", "env-tool"])
    core.console.print("✅ [bold green]Update attempted. Please restart your terminal.[/bold green]")

@main.command()
def uninstall():
    """Completely remove Env Tool from system"""
    core.console.print("🐍 [bold red]Env Tool - Uninstaller[/bold red]", style="bold red")
    if click.confirm("Are you sure you want to uninstall Env Tool?"):
        core.console.print("Uninstalling...")
        core.run_command([sys.executable, "-m", "pip", "uninstall", "env-tool", "-y"])
        core.console.print("✅ [bold green]Env Tool has been uninstalled.[/bold green]")
    else:
        core.console.print("Uninstall cancelled.")

if __name__ == "__main__":
    main()
