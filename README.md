# Telegram Reversi Bot

Python final project: a Telegram bot version of Reversi/Othello with an 8x8 board, player moves, simple AI moves, and conversation-based gameplay.

## Features

- Telegram `/start` command to begin a Reversi game
- 8x8 board display in chat
- Player move validation
- Random legal move selection for the AI opponent
- Piece counting and game result messages
- Experimental inline-button board prototype in `button_basic.py`

## Project Files

- `main.py` - main Telegram Reversi bot
- `2dgame.py` - console prototype of the Reversi game logic
- `button_basic.py` - inline keyboard board prototype
- `conv.py` - conversation-handler learning example
- `bot_secret.example.py` - example token file format, kept without real secrets

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
python main.py
```

## Security Note

Do not commit a real Telegram bot token. This portfolio version reads the token from the `TELEGRAM_BOT_TOKEN` environment variable, and `bot_secret.py` is ignored by Git for local-only use.
