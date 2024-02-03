# STL
from enum import Enum

# LOCAL
from api.constants import BASE_URL


class Search(Enum):
    SEARCH = f"{BASE_URL}/search"


class Playlist(Enum):
    PLAYLIST = f"{BASE_URL}/playlists"


class Endpoints(Enum):
    SEARCH = Search
    PLAYLIST = Playlist
