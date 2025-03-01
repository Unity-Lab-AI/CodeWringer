import click
import subprocess
import sys
import os
import yaml

# Analysis and refactoring imports
from .analysis import analyze_file
from .refactor import refactor_file

@click.group()
def main():
    """CodeWringer CLI - AI-assisted code analysis and refactoring tool."""
    pass

#############################
# Core Code Analysis Commands
#############################

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

#############################
# Git Integration Commands
#############################

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
    """Commit changes to Git with the provided commit message."""
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
@click.argument("repo_url")
def git_clone(repo_url):
    """Clone a repository from the given URL. (Placeholder)"""
    click.echo(f"Placeholder: git clone {repo_url} command not yet implemented.")

@main.command()
def git_pull():
    """Pull the latest changes from the remote repository. (Placeholder)"""
    click.echo("Placeholder: git pull command not yet implemented.")

@main.command()
def git_fetch():
    """Fetch the latest changes from the remote repository. (Placeholder)"""
    click.echo("Placeholder: git fetch command not yet implemented.")

@main.command()
@click.argument("branch")
def git_checkout(branch):
    """Checkout the given branch. (Placeholder)"""
    click.echo(f"Placeholder: git checkout {branch} command not yet implemented.")

@main.command()
def git_push():
    """Push committed changes to the remote repository. (Placeholder)"""
    click.echo("Placeholder: git push command not yet implemented.")

@main.command()
@click.argument("branch")
def git_merge(branch):
    """Merge the specified branch into the current branch. (Placeholder)"""
    click.echo(f"Placeholder: git merge {branch} command not yet implemented.")

@main.command()
@click.argument("mode", type=click.Choice(["soft", "hard"]))
def git_reset(mode):
    """Reset the current branch. Use 'soft' or 'hard'. (Placeholder)"""
    click.echo(f"Placeholder: git reset --{mode} command not yet implemented.")

#############################
# Setup and Diagnostics Commands
#############################

@main.command()
def configure():
    """
    Run the interactive configuration and installation process.
    This re-runs the installer (main_install.py) to allow you to update your model selections and dependencies.
    """
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
    if os.path.exists("config.yaml"):
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        click.echo("Current configuration:")
        click.echo(config)
    else:
        click.echo("No configuration file found (config.yaml).")

@main.command()
def version():
    """Print the version of CodeWringer."""
    try:
        import pkg_resources
        ver = pkg_resources.get_distribution("codewringer").version
        click.echo(f"CodeWringer version: {ver}")
    except Exception:
        click.echo("CodeWringer version not found.")

if __name__ == "__main__":
    main()
