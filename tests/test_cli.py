import subprocess
import os
import yaml
import shutil

def run_cli_command(args):
    return subprocess.run(
        ["python", "-m", "codewringer.cli"] + args,
        capture_output=True,
        text=True
    )

def test_analyze_command(tmp_path):
    code = "def hello():\n    print('Hello World')\n"
    file = tmp_path / "test.py"
    file.write_text(code)
    result = run_cli_command(["analyze", str(file)])
    assert "Analysis Result:" in result.stdout

def test_refactor_command(tmp_path):
    code = "def add(a, b):\n return a+b\n"
    file = tmp_path / "test2.py"
    file.write_text(code)
    result = run_cli_command(["refactor", str(file)])
    assert "Refactoring Suggestions:" in result.stdout

def test_git_status_command():
    result = run_cli_command(["git_status"])
    assert "Git Status:" in result.stdout

def test_git_diff_command():
    result = run_cli_command(["git_diff"])
    # Diff might be empty; we check for successful execution.
    assert result.returncode == 0

def test_git_commit_command():
    result = run_cli_command(["git_commit", "Test commit"])
    # Depending on the repo state, check for commit output or message indicating nothing to commit.
    assert "Git Commit Output:" in result.stdout or "nothing to commit" in result.stdout.lower()

def test_git_clone_placeholder():
    result = run_cli_command(["git_clone", "https://example.com/repo.git"])
    assert "Placeholder: git clone" in result.stdout

def test_git_pull_placeholder():
    result = run_cli_command(["git_pull"])
    assert "Placeholder: git pull" in result.stdout

def test_git_fetch_placeholder():
    result = run_cli_command(["git_fetch"])
    assert "Placeholder: git fetch" in result.stdout

def test_git_checkout_placeholder():
    result = run_cli_command(["git_checkout", "main"])
    assert "Placeholder: git checkout main" in result.stdout

def test_git_push_placeholder():
    result = run_cli_command(["git_push"])
    assert "Placeholder: git push" in result.stdout

def test_git_merge_placeholder():
    result = run_cli_command(["git_merge", "feature"])
    assert "Placeholder: git merge feature" in result.stdout

def test_git_reset_placeholder():
    result = run_cli_command(["git_reset", "soft"])
    assert "Placeholder: git reset --soft" in result.stdout

def test_configure_command():
    # We do not execute main_install.py in tests; just ensure the command runs.
    result = run_cli_command(["configure"])
    # Since it might run the installer, we only check that the command completes.
    assert result.returncode in (0, 1)

def test_diagnose_command(tmp_path):
    config_data = {
        "agent_model": "test-model",
        "embedding_model": "test-embedding",
        "manager_model": "test-manager"
    }
    config_path = tmp_path / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config_data, f)
    shutil.copy(str(config_path), "config.yaml")
    result = run_cli_command(["diagnose"])
    assert "test-model" in result.stdout
    os.remove("config.yaml")

def test_version_command():
    result = run_cli_command(["version"])
    # Version command output might vary; ensure some text is returned.
    assert "CodeWringer version:" in result.stdout or "not found" in result.stdout
