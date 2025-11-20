import os
import requests
from dotenv import load_dotenv
load_dotenv()

PRRESET_API_URL = "https://presence.roblox.com/v1/presence/users"
THUMBNAIL_API_URL = "https://thumbnails.roblox.com/v1/batch"
AVATAR_API_URL = "https://thumbnails.roblox.com/v1/users/avatar-headshot"
USERS_API_URL = "https://users.roblox.com/v1/users"

cookies = os.getenv("cookies")

ses = requests.Session()
if cookies:
    ses.cookies.update({".ROBLOSECURITY": cookies})

ses.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept": "application/json",
})


class Presence():
    def __init__(self, data):
        self.userPresenceType = data.get("userPresenceType")
        self.userId = data.get("userId")
        self.lastLocation = data.get("lastLocation")
        self.placeId = data.get("placeId")
        self.rootPlaceId = data.get("rootPlaceId")
        self.universeId = data.get("universeId")
        self.gameId = data.get("gameId")

    def __repr__(self):
        return f"<Presence userId={self.userId} lastLocation={self.lastLocation} userPresenceType={self.userPresenceType}>"


def get_username(user_id) -> tuple:
    resp = ses.get(f"{USERS_API_URL}/{user_id}")
    resp.raise_for_status()
    data = resp.json()
    # print(data)
    return (data.get("displayName", "RobloxPlayer"), f"@{data.get('name', 'username')} | {data.get('id', 'xxxxxxx')}", "isBanned : "+str(data.get('isBanned', False)))


def get_user_presence(user_id) -> Presence | None:
    resp = ses.post(f"{PRRESET_API_URL}", json={"userIds": [user_id]})
    resp.raise_for_status()
    data = resp.json()
    # print(data)
    if data and "userPresences" in data and data["userPresences"]:
        return Presence(data["userPresences"][0])
    return None


def get_user_avatar(user_id, size="420x420", format="png", isCircular=True):
    params = {
        "userIds": user_id,
        "size": size,
        "format": format,
        "isCircular": str(isCircular).lower(),
    }
    resp = ses.get(AVATAR_API_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data and "data" in data and data["data"]:
        return data["data"][0]["imageUrl"]
    return None


def get_game_thumbnail(universe_id, token="", version="", thumbnailType="GameIcon", size="420x420", format="png"):
    payload = [
        {
            "format": format,
            "requestId": f'{universe_id}::{thumbnailType}::{size}::regular',
            "size": size,
            "targetId": universe_id,
            "token": token,
            "version": version,
            "type": thumbnailType,
        }
    ]
    resp = ses.post(THUMBNAIL_API_URL, json=payload)
    resp.raise_for_status()
    data = resp.json()
    if data["data"]:
        return data["data"][0]["imageUrl"]
    return None


if __name__ == "__main__":
    user_id = 000000

    name = get_username(user_id)
    print("username =", name)
    # presence = get_user_presence(user_id)
    # print(presence)

    # thumbnail_url = get_game_thumbnail(presence.universeId)
    # print("game icon = ",thumbnail_url)

    # avatar_url = get_user_avatar(user_id)
    # print("avatar url =", avatar_url)
