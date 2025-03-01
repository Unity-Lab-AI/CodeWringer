import subprocess
import os
import yaml
import shutil

def test_analyze_command(tmp_path):
    # Create a temporary Python file with simple code.
    code = "def hello():\n    print('Hello World')\n"
    file = tmp_path / "test.py"
    file.write_text(code)
    
    result = subprocess.run(
        ["python", "-m", "codewringer.cli", "analyze", str(file)],
        capture_output=True,
        text=True
    )
    assert "Analysis Result:" in result.stdout

def test_refactor_command(tmp_path):
    code = "def add(a,b):\n return a+b\n"
    file = tmp_path / "test2.py"
    file.write_text(code)
    
    result = subprocess.run(
        ["python", "-m", "codewringer.cli", "refactor", str(file)],
        capture_output=True,
        text=True
    )
    assert "Refactoring Suggestions:" in result.stdout

def test_git_status_command():
    result = subprocess.run(
        ["python", "-m", "codewringer.cli", "git_status"],
        capture_output=True,
        text=True
    )
    # We accept either a normal git status output or a message if not in a git repo
    assert "On branch" in result.stdout or "Not a git repository" in result.stdout

def test_git_diff_command():
    result = subprocess.run(
        ["python", "-m", "codewringer.cli", "git_diff"],
        capture_output=True,
        text=True
    )
    # Diff may be empty; ensure the command executes without error.
    assert result.returncode == 0

def test_git_commit_command():
    # This test will run in a controlled environment.
    result = subprocess.run(
        ["python", "-m", "codewringer.cli", "git_commit", "Test commit"],
        capture_output=True,
        text=True
    )
    # Depending on the repo state, output might indicate nothing to commit.
    assert "Git Commit Output:" in result.stdout or "nothing to commit" in result.stdout.lower()

def test_diagnose_command(tmp_path):
    # Create a temporary config file
    config_data = {
        "agent_model": "test-model",
        "embedding_model": "test-embedding",
        "manager_model": "test-manager"
    }
    config_path = tmp_path / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config_data, f)
    
    # Copy the temporary config.yaml to current working directory
    shutil.copy(str(config_path), "config.yaml")
    
    result = subprocess.run(
        ["python", "-m", "codewringer.cli", "diagnose"],
        capture_output=True,
        text=True
    )
    assert "test-model" in result.stdout
    
    # Clean up the copied config file
    os.remove("config.yaml")
