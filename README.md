# 🤖 TELEGRAM BOT on FastAPI


This project is a Telegram bot that uses FastAPI as the backend, operates via polling, is configured through a .env or YAML file, and includes basic command handling logic and tests.

---

## 📦 Technology

- 🐍 Python 3.10+
- ⚡ FastAPI
- 📡 `python-telegram-bot` (polling mode)
- 🔧 `pydantic` for configuration
- ✅ `pytest` for tests
- 📁 `.env` or `config.yaml` for configuration

---

## 🚀 Functionality

- Communication via the Telegram Bot API
- Launched using polling (webhook support planned)
- Handles commands such as /start, /help, etc.
- Reads settings from a configuration file
- Includes basic tests (e.g. for correct configuration loading)

---

## 🛠️ Instalation

```bash
Clone the forked repo
git clone the-link-from-your-forked-repo

Create a branch for the solution and switch on it
git checkout -b develop

If you are using PyCharm - it may propose you to automatically create venv for your project and install requirements in it, but if not:
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt


# ⚠️Tip: Never store your bot token directly in the code!


## 📚 Usfull links
- [Documentation Telegram Bot API](https://core.telegram.org/bots/api)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [python-telegram-bot] (https://github.com/python-telegram-bot/python-telegram-bot)
