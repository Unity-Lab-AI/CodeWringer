from setuptools import setup, find_packages

setup(
    name="codewringer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click",
        "requests",
        "smolagents",
        "ollama",
        "pyyaml"
    ],
    entry_points={
        "console_scripts": [
            "codewringer=codewringer.cli:main",  # Use lowercase package name
        ],
    },
    author="hackall360",
    description="A CLI tool for AI-assisted code analysis and refactoring using smolagents and Ollama.",
    license="MIT",
    url="https://github.com/YourOrg/codeai-cli",
)
