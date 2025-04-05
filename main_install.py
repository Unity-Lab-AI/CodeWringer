import os
import shutil
import subprocess
import sys
import yaml
import platform

# List of available generation models and embedding models:
GEN_MODELS = [
    "deepseek-r1:1.5b", "deepseek-r1:7b", "deepseek-r1:14b", "deepseek-r1:32b",
    "qwen2.5:3b", "qwen2.5:7b", "qwen2.5:14b", "qwen2.5:32b",
    "qwen2.5-coder:3b-instruct-q4_K_M", "qwen2.5-coder:7b-instruct-q4_K_M",
    "qwen2.5-coder:14b-instruct-q4_K_M", "qwen2.5-coder:32b-instruct-q4_K_M",
    "phi3:3.8b-mini-128k-instruct-q4_K_M", "phi3:14b-medium-128k-instruct-q4_K_M",
    "phi3:3.8b-mini-4k-instruct-q4_K_M", "phi3:14b-medium-4k-instruct-q4_K_M",
    "codellama:13b-code-q4_K_M", "codellama:13b-python-q4_K_M",
    "codellama:34b-code-q4_K_M", "codellama:34b-instruct-q4_K_M",
    "codellama:7b-code-q4_K_M", "codellama:7b-instruct-q4_K_M", "codellama:7b-python-q4_K_M",
    "mistral-nemo:12b-instruct-2407-q4_K_M", "granite3.2:2b-instruct-q4_K_M",
    "granite3.2:8b-instruct-q4_K_M", "deepscaler:1.5b-preview-q4_K_M",
    "dolphin3:8b-llama3.1-q4_K_M"
]

EMBEDDING_MODELS = [
    "nomic-embed-text:latest", "bge-m3:latest", "snowflake-arctic-embed:latest",
    "mxbai-embed-large:latest", "snowflake-arctic-embed2:latest"
]

# Force manager AI to always be installed:
MANAGER_MODEL = "llama3.2"

# CUDA installation commands for various distros with removal of the downloaded keyring file:
CUDA_INSTALL_COMMANDS = {
    "Ubuntu-24.04": (
        "wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb && "
        "sudo dpkg -i cuda-keyring_1.1-1_all.deb && sudo apt-get update && "
        "sudo apt-get -y install cuda-toolkit-12-8 && rm cuda-keyring_1.1-1_all.deb"
    ),
    "Ubuntu-22.04": (
        "wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb && "
        "sudo dpkg -i cuda-keyring_1.1-1_all.deb && sudo apt-get update && "
        "sudo apt-get -y install cuda-toolkit-12-8 && rm cuda-keyring_1.1-1_all.deb"
    ),
    "Ubuntu-20.04": (
        "wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.1-1_all.deb && "
        "sudo dpkg -i cuda-keyring_1.1-1_all.deb && sudo apt-get update && "
        "sudo apt-get -y install cuda-toolkit-12-8 && rm cuda-keyring_1.1-1_all.deb"
    ),
    "Debian-12": (
        "wget https://developer.download.nvidia.com/compute/cuda/repos/debian12/x86_64/cuda-keyring_1.1-1_all.deb && "
        "sudo dpkg -i cuda-keyring_1.1-1_all.deb && sudo apt-get update && "
        "sudo apt-get -y install cuda-toolkit-12-8 && rm cuda-keyring_1.1-1_all.deb"
    ),
    "Fedora-41": (
        "sudo dnf config-manager addrepo --from-repofile https://developer.download.nvidia.com/compute/cuda/repos/fedora41/x86_64/cuda-fedora41.repo && "
        "sudo dnf clean all && sudo dnf -y install cuda-toolkit-12-8"
    ),
    "WSL-Ubuntu": (
        "wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb && "
        "sudo dpkg -i cuda-keyring_1.1-1_all.deb && sudo apt-get update && "
        "sudo apt-get -y install cuda-toolkit-12-8 && rm cuda-keyring_1.1-1_all.deb"
    )
}

def run_command(command):
    """Run a shell command and exit on failure."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Error running command: {command}")
        sys.exit(1)

def install_apt_packages():
    """Ensure required system dependencies are installed.
       Remove any conflicting CUDA source files before updating."""
    print("\n📦 Installing required system packages...")
    # Remove potential conflicting CUDA source files
    run_command("sudo rm -f /etc/apt/sources.list.d/cuda*")
    run_command("sudo apt update")
    run_command("sudo apt install -y curl python3-pip python3-venv git wget unzip")

def detect_linux_distribution():
    """Detect the Linux distribution and version."""
    try:
        info = platform.freedesktop_os_release()
        distro = info["ID"].capitalize()  # e.g., Ubuntu, Debian, Fedora
        version = info["VERSION_ID"]       # e.g., 24.04, 22.04, 12
        return f"{distro}-{version}"
    except Exception:
        return None

def prompt_user_for_cuda():
    """Prompt the user for CUDA installation selection."""
    print("\n🖥️ CUDA installation could not be automatically determined.")
    print("Please select your Linux distribution from the options below:")
    
    options = list(CUDA_INSTALL_COMMANDS.keys())
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("0. Cancel CUDA installation")
    
    choice = input("Enter the number of your OS: ")
    try:
        choice_index = int(choice) - 1
        if choice_index == -1:
            print("❌ CUDA installation canceled.")
            return None
        return options[choice_index]
    except (ValueError, IndexError):
        print("⚠️ Invalid choice. Skipping CUDA installation.")
        return None

def check_and_install_cuda():
    """Check for NVIDIA GPU and install CUDA if needed."""
    print("\n🖥️ Checking for NVIDIA GPU...")
    
    if shutil.which("nvidia-smi"):
        print("✅ NVIDIA GPU detected! Installing CUDA...")
        detected_os = detect_linux_distribution()
        
        if detected_os in CUDA_INSTALL_COMMANDS:
            print(f"🔄 Installing CUDA for detected OS: {detected_os}")
            print("🛠 Removing old CUDA keyrings and source lists...")
            run_command("sudo rm -f /etc/apt/sources.list.d/cuda*")
            run_command("sudo rm -f /usr/share/keyrings/cuda-archive-keyring.gpg")
            run_command(CUDA_INSTALL_COMMANDS[detected_os])
        else:
            selected_os = prompt_user_for_cuda()
            if selected_os:
                print(f"🔄 Installing CUDA for selected OS: {selected_os}")
                print("🛠 Removing old CUDA keyrings and source lists...")
                run_command("sudo rm -f /etc/apt/sources.list.d/cuda*")
                run_command("sudo rm -f /usr/share/keyrings/cuda-archive-keyring.gpg")
                run_command(CUDA_INSTALL_COMMANDS[selected_os])
            else:
                print("❌ Skipping CUDA installation.")
    else:
        print("❌ No NVIDIA GPU detected. Skipping CUDA installation.")

def install_ollama():
    """Check and install Ollama if not present."""
    if not shutil.which("ollama"):
        print("🔄 Installing Ollama...")
        run_command("curl -fsSL https://ollama.com/install.sh | sh")
    else:
        print("✅ Ollama is already installed.")

def install_model(model_name: str):
    """Pull an AI model using Ollama."""
    print(f"📥 Pulling model: {model_name}")
    run_command(f"ollama pull {model_name}")

def interactive_setup():
    """Guide the user through model selection and installation."""
    print("\n🔧 Interactive AI Model Setup")

    print("\n📜 Available AI Generation Models:")
    for idx, model in enumerate(GEN_MODELS, start=1):
        print(f"{idx}: {model}")
    gen_choice = input("Enter the number of the assistant model you wish to use: ")
    try:
        chosen_gen_model = GEN_MODELS[int(gen_choice) - 1]
    except (ValueError, IndexError):
        print("⚠️ Invalid choice; defaulting to qwen2.5-coder:14b-instruct-q4_K_M")
        chosen_gen_model = "qwen2.5-coder:14b-instruct-q4_K_M"

    print("\n📜 Available Embedding Models:")
    for idx, emb in enumerate(EMBEDDING_MODELS, start=1):
        print(f"{idx}: {emb}")
    emb_choice = input("Enter the number of the embedding model you wish to use: ")
    try:
        chosen_embedding = EMBEDDING_MODELS[int(emb_choice) - 1]
    except (ValueError, IndexError):
        print("⚠️ Invalid choice; defaulting to bge-m3:latest")
        chosen_embedding = "bge-m3:latest"

    # Ask user if they want to install additional models
    additional = input("Would you like to pull ALL available generation models? [y/N]: ")
    if additional.lower() == "y":
        for model in GEN_MODELS:
            install_model(model)
    else:
        install_model(chosen_gen_model)

    # Always install manager model
    print(f"\n🔄 Installing manager AI model: {MANAGER_MODEL}")
    install_model(MANAGER_MODEL)
    
    # Pull the chosen embedding model:
    install_model(chosen_embedding)

    # Save configuration
    config = {
        "agent_model": chosen_gen_model,
        "embedding_model": chosen_embedding,
        "manager_model": MANAGER_MODEL
    }
    with open("config.yaml", "w") as f:
        yaml.dump(config, f)
    print("\n✅ Setup complete. Configuration saved to config.yaml.")

if __name__ == "__main__":
    install_apt_packages()
    check_and_install_cuda()
    install_ollama()
    interactive_setup()
