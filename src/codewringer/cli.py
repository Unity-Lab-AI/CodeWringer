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

if __name__ == "__main__":
    main()
