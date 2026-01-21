#!/usr/bin/env python3
"""Bootstrap script to create virtual environment and install dependencies."""

import subprocess
import sys
from pathlib import Path


def main():
    skill_dir = Path(__file__).parent.parent
    venv_path = skill_dir / ".venv"

    print(f"Creating virtual environment at {venv_path}...")
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)

    pip_path = venv_path / "bin" / "pip"
    if not pip_path.exists():
        pip_path = venv_path / "Scripts" / "pip.exe"  # Windows

    print("Installing dependencies...")
    subprocess.run([str(pip_path), "install", "-e", str(skill_dir)], check=True)

    print("\nBootstrap complete!")
    print(f"Use: {venv_path / 'bin' / 'python'} scripts/render_pdf.py --help")


if __name__ == "__main__":
    main()
