# LOCAL
from api.constants import CODE, CLIENT_ID, REDIRECT_URI, CLIENT_SECRET
from api.spotify.Authenticator import Authenticator


class SpotifyClient:
    def __init__(self) -> None:
        self.auth = Authenticator(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, CODE)
        self.token = self.auth.generate_authorization_token()
