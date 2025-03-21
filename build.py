import os
import subprocess
import sys

# Variables
PYTHON = "python"
PIP = "pip"
FLASK_APP = "app.py"
STATIC_DIR = "static"
TEMPLATES_DIR = "templates"
REQUIREMENTS = "requirements.txt"
TEST_FILE = "test_backEndShopLyft.py"
VENV_DIR = "venv"  # Virtual environment directory

def run_command(command, shell=True):
    """Helper function to run shell commands."""
    result = subprocess.run(command, shell=shell, text=True)
    if result.returncode != 0:
        print(f"Error: Command failed: {command}")
        sys.exit(1)

def install():
    """Set up virtual environment and install dependencies."""
    print("Setting up virtual environment...")
    run_command(f"{PYTHON} -m venv {VENV_DIR}")
    
    # Activate virtual environment and install dependencies
    if os.name == "nt":  # Windows
        activate_script = os.path.join(VENV_DIR, "Scripts", "activate")
    else:  # macOS/Linux
        activate_script = os.path.join(VENV_DIR, "bin", "activate")
    
    print("Installing dependencies...")
    run_command(f"{activate_script} && {PIP} install -r {REQUIREMENTS}")

def run():
    """Run the Flask application."""
    print("Starting Flask application...")
    if os.name == "nt":  # Windows
        activate_script = os.path.join(VENV_DIR, "Scripts", "activate")
    else:  # macOS/Linux
        activate_script = os.path.join(VENV_DIR, "bin", "activate")
    
    run_command(f"{activate_script} && set FLASK_APP={FLASK_APP} && flask run")

def clean(remove_images=False):
    """Clean up generated files."""
    print("Cleaning up...")
    
    # Remove __pycache__ directories
    if os.path.exists("__pycache__"):
        run_command(f"rmdir /s /q __pycache__" if os.name == "nt" else f"rm -rf __pycache__")
    
    # Optionally remove PNG files in static/images (but please don't do this for the love of god)
    if remove_images and os.path.exists(os.path.join(STATIC_DIR, "images")):
        print("Removing images...")
        for file in os.listdir(os.path.join(STATIC_DIR, "images")):
            if file.endswith(".png"):
                os.remove(os.path.join(STATIC_DIR, "images", file))
        print("Images removed.")
    
    # Remove requirements.txt
    if os.path.exists(REQUIREMENTS):
        os.remove(REQUIREMENTS)

def freeze(): 
    """Generate requirements.txt."""
    print("Generating requirements.txt...")
    if os.name == "nt":  # Windows
        activate_script = os.path.join(VENV_DIR, "Scripts", "activate")
    else:  # macOS/Linux
        activate_script = os.path.join(VENV_DIR, "bin", "activate")
    
    run_command(f"{activate_script} && {PIP} freeze > {REQUIREMENTS}")

def test():
    """Run tests from test_backEndShopLyft.py."""
    print(f"Running tests from {TEST_FILE}...")
    if os.name == "nt":  # Windows
        activate_script = os.path.join(VENV_DIR, "Scripts", "activate")
    else:  # macOS/Linux
        activate_script = os.path.join(VENV_DIR, "bin", "activate")
    
    run_command(f"{activate_script} && {PYTHON} -m unittest {TEST_FILE}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build.py <command>")
        print("Commands: install, run, clean (or clean --remove-images), freeze, test")
        sys.exit(1)

    command = sys.argv[1]
    if command == "install":
        install()
    elif command == "run":
        run()
    elif command == "clean":
        # Optional: Pass --remove-images to clean PNG files
        remove_images = "--remove-images" in sys.argv
        clean(remove_images=remove_images)
    elif command == "freeze":
        freeze()
    elif command == "test":
        test()
    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)