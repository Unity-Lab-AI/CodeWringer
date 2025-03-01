import click
import subprocess
from .analysis import analyze_file
from .refactor import refactor_file

@click.group()
def main():
    """CodeWringer CLI - AI-assisted code analysis and refactoring tool."""
    pass

@main.command()
@click.argument('file_path', type=click.Path(exists=True))
def analyze(file_path):
    """Analyze the given code file for potential improvements."""
    result = analyze_file(file_path)
    click.echo("Analysis Result:")
    click.echo(result)

@main.command()
@click.argument('file_path', type=click.Path(exists=True))
def refactor(file_path):
    """Provide refactoring suggestions for the given code file."""
    result = refactor_file(file_path)
    click.echo("Refactoring Suggestions:")
    click.echo(result)

@main.command()
def git_status():
    """Show the current Git status of the repository."""
    try:
        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True,
            check=True
        )
        click.echo("Git Status:")
        click.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        click.echo("Error running git status:")
        click.echo(e.output)

@main.command()
def git_diff():
    """Show the Git diff for the repository."""
    try:
        result = subprocess.run(
            ["git", "diff"],
            capture_output=True,
            text=True,
            check=True
        )
        click.echo("Git Diff:")
        click.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        click.echo("Error running git diff:")
        click.echo(e.output)

@main.command()
@click.argument("message")
def git_commit(message):
    """Commit changes to Git with a provided commit message."""
    try:
        result = subprocess.run(
            ["git", "commit", "-am", message],
            capture_output=True,
            text=True,
            check=True
        )
        click.echo("Git Commit Output:")
        click.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        click.echo("Error running git commit:")
        click.echo(e.output)

@main.command()
def configure():
    """
    Run the interactive configuration and installation process.
    This re-runs the installer (main_install.py) to allow you to update your model selections and dependencies.
    """
    import sys
    try:
        subprocess.run([sys.executable, "main_install.py"], check=True)
    except subprocess.CalledProcessError as e:
        click.echo("Error during configuration:")
        click.echo(e.output)

@main.command()
def diagnose():
    """
    Print the current configuration from config.yaml.
    This helps in troubleshooting by displaying the chosen models and settings.
    """
    import os
    import yaml
    if os.path.exists("config.yaml"):
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        click.echo("Current configuration:")
        click.echo(config)
    else:
        click.echo("No configuration file found (config.yaml).")

if __name__ == "__main__":
    main()
