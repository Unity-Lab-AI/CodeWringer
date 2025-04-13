import click
from src.framework.manager import ManagerAgent
from src.utils.helpers import load_config

@click.group()
def cli():
    """CODEWRINGER CLI - AI-assisted code analysis and refactoring tool."""
    pass

@cli.command()
@click.argument("task")
def run(task):
    """Run a task using the manager agent."""
    config = load_config("config.yaml")
    if not config:
        click.echo("Error: Failed to load config.yaml")
        return

    manager = ManagerAgent(config)
    result = manager.run_task(task)
    click.echo(f"Result: {result}")

@cli.command()
def config():
    """Display the current configuration."""
    config = load_config("config.yaml")
    if config:
        click.echo("Current Configuration:")
        for key, value in config.items():
            click.echo(f"{key}: {value}")
    else:
        click.echo("Error: Failed to load config.yaml")

if __name__ == "__main__":
    cli()