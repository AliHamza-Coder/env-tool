import click
import json
import sys
import shutil
import os
from rich.table import Table
from rich.tree import Tree
from envtool import core, __version__

@click.group(invoke_without_command=True, context_settings=dict(help_option_names=['-h', '--help']))
@click.option("--debug", is_flag=True, help="Show full stack Traces and detailed logs")
@click.option("--python", "python_path", help="Specify Python version/path for venv creation")
@click.pass_context
def main(ctx, debug, python_path):
    """🐍 Env Tool - Professional Python Virtual Environment Manager
    
    Developed by Ali Hamza
    """
    core.set_debug(debug)
    if python_path:
        os.environ["ENVTOOL_PYTHON"] = python_path
    
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
@click.option("--tree", is_flag=True, help="Show dependencies in a tree view")
def list(tree):
    """List all installed packages and their versions"""
    if tree:
        display_dependency_tree()
    else:
        core.list_dependencies()

def display_dependency_tree():
    """Display a hierarchical tree of installed packages"""
    is_active = core.is_venv_active()
    context_name = f"Environment: [bold cyan]{core.ENV_NAME}[/bold cyan]" if is_active else "Environment: [bold yellow]Global[/bold yellow]"
    
    python_exe = core.get_python_exe() if is_active else sys.executable
    
    with core.console.status(f"[dim]Building dependency tree for {context_name}...", spinner="dots"):
        # We use a trick: run a small script inside the venv to build the tree using importlib.metadata
        script = """
import importlib.metadata
import json
import sys

def get_tree():
    pkgs = importlib.metadata.distributions()
    tree = {}
    all_deps = set()
    
    for dist in pkgs:
        name = dist.metadata['Name']
        version = dist.version
        requires = dist.requires or []
        deps = []
        for r in requires:
            dep_name = r.split()[0].split('>')[0].split('=')[0].split('<')[0]
            deps.append(dep_name)
            all_deps.add(dep_name)
        tree[name] = {"version": version, "deps": deps}
    
    # Identify top-level packages (not a dependency of anything else)
    top_level = [n for n in tree.keys() if n not in all_deps]
    return {"tree": tree, "top_level": top_level}

print(json.dumps(get_tree()))
"""
        result = core.run_command([str(python_exe), "-c", script], capture_output=True)
        
    if not result:
        core.console.print("[red]Failed to build dependency tree.[/red]")
        return

    try:
        data = json.loads(result.stdout)
        pkg_tree = data['tree']
        top_level = data['top_level']
        
        tree_display = Tree(f"📦 {context_name}")
        
        def add_nodes(parent_node, pkg_name, visited=None):
            if visited is None: visited = set()
            if pkg_name in visited: return
            visited.add(pkg_name)
            
            info = pkg_tree.get(pkg_name)
            if not info: return
            
            current_node = parent_node.add(f"[cyan]{pkg_name}[/cyan] [dim]({info['version']})[/dim]")
            for dep in info['deps']:
                add_nodes(current_node, dep, visited.copy())

        for pkg in sorted(top_level):
            add_nodes(tree_display, pkg)
            
        core.console.print("\n")
        core.console.print(tree_display)
        core.console.print("\n")
    except Exception as e:
        core.console.print(f"[red]Error parsing tree data: {e}[/red]")

@main.command()
def net():
    """Check internet connectivity status"""
    core.display_network_status()

@main.command()
@click.pass_context
def help(ctx):
    """Show this help message and exit"""
    core.console.print("\n🐍 [bold green]Env Tool - Command Reference[/bold green]\n")
    
    table = Table(box=None, show_header=False, padding=(0, 2))
    table.add_column("Command", style="bold cyan")
    table.add_column("Description", style="dim")

    for name, command in main.commands.items():
        if name == 'help': continue
        help_text = command.get_short_help_str() or ""
        table.add_row(name, help_text)
    
    table.add_row("g", "Global Environment Management (Store)")

    core.console.print(table)
    core.console.print("\n[dim]Use [bold cyan]env <command> --help[/bold cyan] for more details.[/dim]\n")

@main.command()
@click.option("--path", is_flag=True, help="Print only the path to the activation script")
def a(path):
    """Activate the virtual environment"""
    venv_path = core.get_venv_path()
    if not venv_path.exists():
        if not path:
            core.console.print("[bold red]Venv not found.[/bold red] Run [bold cyan]env[/bold cyan] first to create it.")
        return

    try:
        display_path = venv_path.relative_to(core.Path.cwd())
        prefix = ".\\" if sys.platform == "win32" else "./"
        display_str = f"{prefix}{display_path}"
    except ValueError:
        display_str = str(venv_path)

    if sys.platform == "win32":
        act_script = venv_path / "Scripts" / "Activate.ps1"
        if not act_script.exists():
             act_script = venv_path / "Scripts" / "activate.bat"
        
        if path:
            click.echo(str(act_script))
        else:
            core.console.print("\n🐍 [bold green]Activation Command:[/bold green]")
            core.console.print(f"[bold yellow]{display_str}\\Scripts\\activate[/bold yellow]\n")
    else:
        act_script = venv_path / "bin" / "activate"
        if path:
            click.echo(str(act_script))
        else:
            core.console.print("\n🐍 [bold green]Activation Command:[/bold green]")
            core.console.print(f"[bold yellow]source {display_str}/bin/activate[/bold yellow]\n")

@main.command()
def d():
    """Deactivate the virtual environment"""
    core.console.print("\n🐍 [bold red]Deactivation Command:[/bold red]")
    core.console.print("[bold yellow]deactivate[/bold yellow]\n")

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
@click.option("--shell", is_flag=True, help="Run command inside a system shell (enables pipes/redirects)")
def run(command, shell):
    """Execute a command inside the virtual environment"""
    cmd_list = list(command)
    if shell:
        # Re-join command for shell execution
        full_command = " ".join(cmd_list)
        python_exe = core.get_python_exe()
        # Simple substitution for 'python' keyword
        if full_command.startswith("python"):
            full_command = full_command.replace("python", str(python_exe), 1)
        core.run_command([full_command], shell=True)
    else:
        core.run_in_venv(cmd_list)

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
    
    with core.console.status("[dim]Checking for updates...", spinner="dots"):
        latest = core.check_latest_version()
    
    if latest and latest not in ["offline", "limit", "ssl_error", "timeout"] and not latest.startswith("error"):
        if latest != __version__:
            core.console.print(f"\n[bold yellow]🔔 A new version is available: {latest}[/bold yellow]")
            core.console.print(f"Run [bold cyan]env upgrade[/bold cyan] to update instantly.\n")
        else:
            core.console.print("[dim](You are on the latest version)[/dim]\n")
    else:
        if latest == "offline":
            core.console.print("[dim](Version check skipped: Offline)[/dim]\n")
        elif latest == "ssl_error":
            core.console.print("[dim](Version check skipped: SSL/Security Error)[/dim]\n")
        elif latest == "limit":
            core.console.print("[dim](Version check skipped: GitHub API Rate Limit)[/dim]\n")
        elif latest == "timeout":
            core.console.print("[dim](Version check skipped: Request Timeout)[/dim]\n")
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
    
    if not latest or latest in ["offline", "ssl_error", "limit", "timeout"] or latest.startswith("error") or latest.startswith("http_error"):
        if latest == "offline":
             core.console.print("[bold red]❌ Offline Mode[/bold red]")
             core.console.print("[yellow]You are not connected to the internet.[/yellow]")
        elif latest == "ssl_error":
            core.console.print("[bold red]❌ Security/SSL Error[/bold red]")
            core.console.print("[yellow]Could not verify secure connection to GitHub. Check your system clock or firewall.[/yellow]")
        elif latest == "limit":
            core.console.print("[bold yellow]🔔 Rate Limit Reached[/bold yellow]")
            core.console.print("[dim]GitHub API is temporarily limiting requests. Try again in a few minutes.[/dim]")
        elif latest == "timeout":
            core.console.print("[bold red]❌ Request Timeout[/bold red]")
            core.console.print("[yellow]The request to GitHub timed out. Connection may be too slow.[/yellow]")
        else:
            core.console.print("[bold red]❌ Connection Error[/bold red]")
            error_m = latest.split(":", 1)[1] if latest and ":" in latest else latest
            core.console.print(f"[yellow]Could not reach GitHub updates: {error_m}[/yellow]")
        
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
    core.run_command([sys.executable, "-m", "pip", "install", "--upgrade", "env-tool", "--no-cache-dir"])
    core.console.print("✅ [bold green]Upgrade command executed. Please restart your terminal to see changes.[/bold green]")

@main.command()
def uninstall():
    """Completely remove Env Tool from system"""
    core.console.print("🐍 [bold red]Env Tool - Uninstaller[/bold red]", style="bold red")
    
    env_binary = shutil.which("env")
    
    if click.confirm("\n⚠️ This will remove Env Tool and all its shortcuts. Proceed?"):
        core.console.print("Uninstalling package via pip...", style="dim")
        core.run_command([sys.executable, "-m", "pip", "uninstall", "env-tool", "-y"])
        
        if sys.platform == "win32" and env_binary:
            binary_path = core.Path(env_binary)
            # Only delete if it's in a Python Scripts directory (standard pip location)
            if "Scripts" in str(binary_path):
                scripts_dir = binary_path.parent
                patterns = ["env.exe", "env-script.py", "env.cmd", "env.ps1"]
                cleaned = []
                
                for p in patterns:
                    file_to_del = scripts_dir / p
                    if file_to_del.exists():
                        try:
                            file_to_del.unlink()
                            cleaned.append(p)
                        except Exception:
                            pass
                
                if cleaned:
                    core.console.print(f"🧹 Cleaned leftovers: [dim]{', '.join(cleaned)}[/dim]")

        core.console.print("\n✅ [bold green]Env Tool has been thoroughly uninstalled.[/bold green]")
        core.console.print("[yellow]Note: You may need to restart your terminal.[/yellow]")
    else:
        core.console.print("Uninstall cancelled.")

@main.command()
def completion():
    """Generate shell completion instructions"""
    core.console.print("\n🐍 [bold green]Env Tool - Shell Completion[/bold green]")
    core.console.print("To enable tab completion, add the following to your profile:\n")
    
    if sys.platform == "win32":
        core.console.print("[bold cyan]PowerShell ($PROFILE):[/bold cyan]")
        core.console.print('Register-ArgumentCompleter -CommandName env -ScriptBlock {')
        core.console.print('    param($wordToComplete, $commandAst, $cursorPosition)')
        core.console.print('    # Basic completion for main commands')
        core.console.print('    $cmds = "list", "net", "a", "d", "run", "freeze", "update", "clean", "init", "version", "upgrade", "uninstall", "g"')
        core.console.print('    $cmds | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object { [System.Management.Automation.CompletionResult]::new($_, $_, "ParameterValue", $_) }')
        core.console.print('}')
    else:
        core.console.print("[bold cyan]Bash (~/.bashrc):[/bold cyan]")
        core.console.print('eval "$(_ENV_COMPLETE=bash_source env)"')
        core.console.print("\n[bold cyan]Zsh (~/.zshrc):[/bold cyan]")
        core.console.print('eval "$(_ENV_COMPLETE=zsh_source env)"')

@main.group()
def g():
    """Global Environment Management (Central Store)"""
    pass

@g.command(name="create")
@click.argument("name")
def g_create(name):
    """Create a new global virtual environment"""
    core.console.print("🌍 [bold green]Env Tool - Create Global Environment[/bold green]")
    core.create_global_venv(name)

@g.command(name="list")
def g_list():
    """List all global virtual environments"""
    core.console.print("🌍 [bold green]Env Tool - Global Store[/bold green]")
    core.list_global_envs()

@g.command(name="use")
@click.argument("name")
def g_use(name):
    """Link current project to a global environment"""
    core.console.print("🌍 [bold green]Env Tool - Global Linking[/bold green]")
    core.link_project_to_global(name)

@g.command(name="clean")
@click.argument("name", required=False)
@click.option("--all", "remove_all", is_flag=True, help="Remove all global environments")
def g_clean(name, remove_all):
    """Delete specific or all global environments"""
    core.console.print("🌍 [bold red]Env Tool - Global Cleanup[/bold red]")
    if not name and not remove_all:
        core.console.print("[yellow]Please specify an environment name or use --all.[/yellow]")
        return
        
    confirm_msg = "Are you sure you want to delete ALL global environments?" if remove_all else f"Are you sure you want to delete global environment '{name}'?"
    if click.confirm(confirm_msg):
        core.remove_global_venv(name, remove_all)

if __name__ == "__main__":
    main()
