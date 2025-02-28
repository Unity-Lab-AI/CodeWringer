import subprocess
import sys

REQUIRED_PACKAGES = ["pyyaml"]  # All others (shutil, os, platform, etc.) are part of the stdlib

def is_installed(package):
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def install_missing_packages():
    missing = [pkg for pkg in REQUIRED_PACKAGES if not is_installed(pkg)]
    if missing:
        print(f"📦 Installing missing Python packages: {', '.join(missing)}")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing, check=True)
    else:
        print("✅ All Python dependencies are already installed.")

if __name__ == "__main__":
    install_missing_packages()
    subprocess.run([sys.executable, "main_install.py"], check=True)
