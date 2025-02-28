import subprocess

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
    # Check if git status output contains expected text
    assert "On branch" in result.stdout or "Not a git repository" in result.stdout
