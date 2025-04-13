import sys
from src.framework.cli import cli
from src.framework.manager import ManagerAgent
from src.utils.helpers import load_config

def main():
    # Load configuration
    config = load_config("config.yaml")
    if not config:
        sys.exit(1)

    # If command-line arguments are provided, run the CLI
    if len(sys.argv) > 1:
        cli()
    else:
        # Otherwise, initialize the manager agent and run a default task
        manager = ManagerAgent(config)
        task = "Analyze and refactor a sample Python file."
        result = manager.run_task(task)
        print(f"Manager Result: {result}")

if __name__ == "__main__":
    main()