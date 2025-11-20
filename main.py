from utils.api import get_game_thumbnail, get_user_avatar, get_user_presence, get_username
from utils.image import create_status_image
from dotenv import load_dotenv
import os
from whatsapp_api_client_python import API

load_dotenv()

os.remove("status.png") if os.path.exists("status.png") else None

GREENAPI_INSTANCE = os.getenv("GREENAPI_INSTANCE")
GREENAPI_API_KEY = os.getenv("GREENAPI_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")

greenAPI = API.GreenAPI(GREENAPI_INSTANCE, GREENAPI_API_KEY)

user_id = 8745776116
presence = get_user_presence(user_id)
print(presence)

username, additional_info, is_banned = get_username(user_id)
status = "Offline"
game_name = None
avatar_url = get_user_avatar(user_id)
game_icon = None

if presence.userPresenceType == 0:
    status = "Offline"
elif presence.userPresenceType == 1:
    status = "Online"
    game_name = "Website"
    game_icon = "https://t3.rbxcdn.com/180DAY-e559fde711d62cc11604158b5f39187c"
elif presence.userPresenceType == 2:
    status = "Online"
    if presence.placeId and presence.universeId:
        game_icon = get_game_thumbnail(presence.universeId)
        game_name = presence.lastLocation

create_status_image(
    username=username,
    status=status,
    game_name=game_name,
    additional_info=additional_info,
    avatar_url=avatar_url,
    game_icon_url=game_icon,
    is_banned=is_banned
)

greenAPI.sending.sendFileByUpload(
    CHAT_ID,
    "status.png",
    "status.png",
    ""
)
