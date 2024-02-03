# STL
import re

# PDM
import requests
from fastapi import Request, APIRouter

# LOCAL
from api.spotify.Endpoints import Playlist, Endpoints
from api.spotify.SpotifyClient import SpotifyClient

spotify_router = APIRouter()

spotify = SpotifyClient()
spotify.auth.generate_authorization_token()


@spotify_router.get("/spotify/playlist")
async def get_playlist(request: Request):
    res = await request.json()
    assert res.get("url")

    url = res.get("url")

    ID = re.search(r"/playlist/([^?]+)", url)
    if ID:
        ID = ID.group(1)

    bearer_token = f"Bearer {spotify.auth.access_token}"
    headers = {"Authorization": bearer_token}

    playlist = Endpoints.PLAYLIST.value
    playlist = f"{playlist.PLAYLIST.value}/{ID}"

    res = requests.get(playlist, headers=headers)
    return res.json()
