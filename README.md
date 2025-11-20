# WA Bot Roblox Tracker

Lightweight script that checks a Roblox user's presence, renders a status image, and sends it to a WhatsApp chat via Green API.

## Features
- Fetches Roblox user info and presence via [`utils.api.get_user_presence`](utils/api.py) and [`utils.api.get_username`](utils/api.py).
- Retrieves avatar and game icons via [`utils.api.get_user_avatar`](utils/api.py) and [`utils.api.get_game_thumbnail`](utils/api.py).
- Renders a status image with [`utils.image.create_status_image`](utils/image.py).
- Sends the generated `status.png` using Green API in [main.py](main.py).

## Prerequisites
- Python 3.8+
- System fonts used by the script (the code currently expects `GothamBlack.otf` in working dir or system font path).
- Create a virtualenv recommended.

## Install Python dependencies:
```bash
pip install pillow requests python-dotenv whatsapp_api_client_python
```

## Configuration
Copy the example env and fill values:
```
cp example.env .env
```
- cookies — your .ROBLOSECURITY cookie (keep private).
- GREENAPI_INSTANCE — Green API instance ID.
- GREENAPI_API_KEY — Green API API key.
- CHAT_ID — target WhatsApp chat id.

