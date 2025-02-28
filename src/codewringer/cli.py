import click
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

if __name__ == "__main__":
    main()
