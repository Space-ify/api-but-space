# STL
import re

# PDM
import requests
from fastapi import Request, APIRouter
from starlette.responses import FileResponse

# LOCAL
from api.utils import image_to_base64_string
from api.spotify.Endpoints import Playlist, Endpoints
from api.generator.Transformer import Transformer
from api.spotify.SpotifyClient import SpotifyClient

spotify_router = APIRouter()

spotify = SpotifyClient()


@spotify_router.post("/api/spotify/playlist")
async def get_playlist(request: Request):
    spotify.auth.generate_authorization_token()

    res = await request.json()
    assert res.get("url")

    url = res.get("url")

    ID = re.search(r"/playlist/([^?]+)", url.get("query"))
    if ID:
        ID = ID.group(1)

    bearer_token = f"Bearer {spotify.auth.access_token}"
    headers = {"Authorization": bearer_token}

    playlist = Endpoints.PLAYLIST.value
    playlist = f"{playlist.PLAYLIST.value}/{ID}"

    res = requests.get(playlist, headers=headers)

    try:
        t = Transformer(res.json())
        return {"items": t.tracklist}
    except:
        return {"message": "Error parsing tracks."}
