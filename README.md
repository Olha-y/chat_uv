# TELEGRAM BOT on FastAPI


This project is Personal Telegram Bot for a single user.
It works as a handy tool for quick access to data by item code or product name.

---

## Technology

- Python 3.10+
- FastAPI
- pytest

---

## Functionality

- Communication via the Telegram Bot API
- Launched using polling (webhook support planned)
- Handles commands such as /start, /help, etc.
- Reads settings from a configuration file
- Includes basic tests (e.g. for correct configuration loading)

---

## Instalation

In this project we use uv package manager. 
If you don't use it before, you can install it with standalone installers:
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

Or, from PyPI:
# With pip.
pip install uv
# Or pipx.
pipx install uv

uv venv              # Create a virtual environment
source .venv/bin/activate  # Activate the environment (on Linux/macOS)
💡 On Windows, use:
.\.venv\Scripts\activate

uv sync    # Install all dependencies from lock file


# Tip: Never store your bot token directly in the code!

