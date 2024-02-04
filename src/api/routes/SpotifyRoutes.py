# STL
import re

# PDM
import requests
from fastapi import Request, APIRouter
from starlette.responses import FileResponse

# LOCAL
from api.utils import image_to_base64_string
from api.spotify.Endpoints import Playlist, Endpoints
from api.spotify.SpotifyClient import SpotifyClient

spotify_router = APIRouter()

spotify = SpotifyClient()
spotify.auth.generate_authorization_token()

img_data = image_to_base64_string("./images/test.png")

test_data = [
    {
        "id": 0,
        "color": "#9ade4d",
        "xRadius": 6.0,
        "zRadius": 3.0,
        "size": 0.5117531328164235,
        "speed": 0.46085133373814036,
        "offset": 3.482799921154449,
        "rotationSpeed": 0.022596633190025132,
        "textureMap": img_data,
        "name": "song name",
    },
    {
        "id": 1,
        "color": "#9e198f",
        "xRadius": 10.0,
        "zRadius": 5.0,
        "size": 0.7641251877394797,
        "speed": 0.20200118740156534,
        "offset": 4.406875651482467,
        "rotationSpeed": 0.016165443883576602,
        "textureMap": img_data,
        "name": "song name",
    },
    {
        "id": 2,
        "color": "#1231ed",
        "xRadius": 14.0,
        "zRadius": 7.0,
        "size": 0.7502969827656718,
        "speed": 0.5275380391629294,
        "offset": 2.8235732227211616,
        "rotationSpeed": 0.02174475572870173,
        "textureMap": img_data,
        "name": "song name",
    },
    {
        "id": 3,
        "color": "#9e7bf8",
        "xRadius": 18.0,
        "zRadius": 9.0,
        "size": 0.7004943339290939,
        "speed": 0.5340610153477514,
        "offset": 3.934133842877386,
        "rotationSpeed": 0.025821059626857164,
        "textureMap": img_data,
        "name": "song name",
    },
    {
        "id": 4,
        "color": "#7e5f5e",
        "xRadius": 22.0,
        "zRadius": 11.0,
        "size": 0.6440945127696011,
        "speed": 0.3768739883398593,
        "offset": 1.8491380629579632,
        "rotationSpeed": 0.021119579521238392,
        "textureMap": img_data,
        "name": "song name",
    },
    {
        "id": 5,
        "color": "#ef478c",
        "xRadius": 26.0,
        "zRadius": 13.0,
        "size": 0.9260469179480473,
        "speed": 0.33191116037862867,
        "offset": 0.6022026892915877,
        "rotationSpeed": 0.012529780287854503,
        "textureMap": img_data,
        "name": "song name",
    },
]


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


@spotify_router.get("/spotify/test")
async def test():
    return {"items": test_data}
