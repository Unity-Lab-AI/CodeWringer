import subprocess
import logging
import tempfile
import os

metadata = {
    "name": "compile",
    "description": "Compiles and runs Python code, capturing outputs and errors."
}

def execute(task: str) -> str:
    logger = logging.getLogger("CompileTool")
    try:
        # Write code to a temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(task)
            temp_file = f.name

        # Run the code
        result = subprocess.run(["python", temp_file], capture_output=True, text=True)
        os.remove(temp_file)

        if result.returncode == 0:
            logger.info("Code executed successfully.")
            return f"Output:\n{result.stdout}"
        else:
            logger.error(f"Code execution failed: {result.stderr}")
            return f"Error:\n{result.stderr}"
    except Exception as e:
        logger.error(f"Compile tool error: {e}")
        return f"Error: {str(e)}"