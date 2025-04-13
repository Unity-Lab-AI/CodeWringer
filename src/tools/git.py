import subprocess
import logging

metadata = {
    "name": "git",
    "description": "Handles Git operations such as status, commit, and push."
}

def execute(task: str) -> str:
    logger = logging.getLogger("GitTool")
    try:
        if "status" in task.lower():
            result = subprocess.run(["git", "status"], capture_output=True, text=True, check=True)
            logger.info("Git status executed successfully.")
            return result.stdout
        elif "commit" in task.lower():
            # Extract message if provided, else use default
            message = "Automated commit" if "commit" not in task else task.split("commit", 1)[1].strip()
            result = subprocess.run(["git", "commit", "-am", message], capture_output=True, text=True, check=True)
            logger.info(f"Git commit executed with message: {message}")
            return result.stdout
        elif "push" in task.lower():
            result = subprocess.run(["git", "push"], capture_output=True, text=True, check=True)
            logger.info("Git push executed successfully.")
            return result.stdout
        else:
            return "Unsupported Git operation."
    except subprocess.CalledProcessError as e:
        logger.error(f"Git operation failed: {e}")
        return f"Error: {e.output}"