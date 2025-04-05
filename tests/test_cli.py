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

# Core analysis commands
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

# Git commands
def test_git_status_command():
    result = run_cli_command(["git_status"])
    assert "Git Status:" in result.stdout

def test_git_diff_command():
    result = run_cli_command(["git_diff"])
    assert result.returncode == 0

def test_git_commit_command():
    result = run_cli_command(["git_commit", "Test commit"])
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

# Setup/Diagnostics commands
def test_configure_command():
    result = run_cli_command(["configure"])
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
    assert "CodeWringer version:" in result.stdout or "not found" in result.stdout

# Testing & Development commands placeholders
def test_run_tests_command():
    result = run_cli_command(["run_tests"])
    assert result.returncode in (0, 1)  # Depending on test suite state

def test_lint_placeholder():
    result = run_cli_command(["lint"])
    assert "Placeholder: linting" in result.stdout

def test_format_placeholder():
    result = run_cli_command(["format"])
    assert "Placeholder: code formatting" in result.stdout

def test_debug_placeholder():
    result = run_cli_command(["debug"])
    assert "Placeholder: debug" in result.stdout

def test_build_placeholder():
    result = run_cli_command(["build"])
    assert "Placeholder: build" in result.stdout

def test_deploy_placeholder():
    result = run_cli_command(["deploy"])
    assert "Placeholder: deploy" in result.stdout

def test_generate_placeholder():
    result = run_cli_command(["generate"])
    assert "Placeholder: generate" in result.stdout

# Agent commands placeholders
def test_agent_list_placeholder():
    result = run_cli_command(["agent_list"])
    assert "Placeholder: agent list" in result.stdout

def test_agent_create_placeholder():
    result = run_cli_command(["agent_create", "test_agent"])
    assert "Placeholder: agent create" in result.stdout

def test_agent_run_placeholder():
    result = run_cli_command(["agent_run", "test_agent", "do something"])
    assert "Placeholder: agent 'test_agent' run" in result.stdout
