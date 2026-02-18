import click
import sys
from envtool import core, __version__

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """🐍 Env Tool - Professional Python Virtual Environment Manager"""
    if ctx.invoked_subcommand is None:
        # Default behavior: Setup environment
        click.secho("\n🐍 Env Tool - Setting up Environment", fg="green", bold=True)
        core.create_venv()
        core.upgrade_pip()
        core.install_requirements()
        click.secho("\n✅ Environment Ready and Active.", fg="green")
        
        # Activation tip
        if sys.platform == "win32":
            click.secho("\nTip: To activate manually, run: myenv\\Scripts\\activate", fg="yellow")
        else:
            click.secho("\nTip: To activate manually, run: source myenv/bin/activate", fg="yellow")
    else:
        pass

@main.command()
def help_cmd():
    """Show help message"""
    with click.Context(main) as ctx:
        click.echo(main.get_help(ctx))

@main.command()
def freeze():
    """Export dependencies to requirements.txt"""
    click.secho("🐍 Env Tool - Freeze Dependencies", fg="green")
    success, message = core.freeze_dependencies()
    if success:
        click.secho(f"✅ {message}", fg="green")
    else:
        click.secho(f"❌ {message}", fg="red")

@main.command()
def update():
    """Update all packages to latest versions"""
    click.secho("🐍 Env Tool - Update Environment", fg="green")
    success, message = core.update_dependencies()
    if success:
        click.secho(f"✅ {message}", fg="green")
    else:
        click.secho(message, fg="red")

@main.command()
def version():
    """Show Env Tool and Python version info"""
    click.secho("🐍 Env Tool - Version Information", fg="green")
    click.echo(f"Current Env Tool Version: {__version__}")
    
    python_ver = core.run_command([sys.executable, "--version"], capture_output=True)
    if python_ver:
        click.echo(f"Global Python version: {python_ver.stdout.strip()}")
    
    env_python = core.get_python_exe()
    if env_python.exists():
        env_ver = core.run_command([str(env_python), "--version"], capture_output=True)
        if env_ver:
            click.echo(f"Environment Python version: {env_ver.stdout.strip()}")

@main.command()
def self_update():
    """Update Env Tool to latest version"""
    click.secho("🐍 Env Tool - Self Update", fg="green")
    click.echo("Updating via pip...")
    # Since we'll install this via pip now, self-update is just running pip install --upgrade env-tool
    core.run_command([sys.executable, "-m", "pip", "install", "--upgrade", "env-tool"])
    click.secho("✅ Update attempted. Please restart your terminal.", fg="green")

if __name__ == "__main__":
    main()
