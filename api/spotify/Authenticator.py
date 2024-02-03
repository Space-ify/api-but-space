# PDM
import requests


class Authenticator:
    def __init__(self, CLIENT_ID: str, CLIENT_SECRET: str) -> None:
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.access_token = None
        self.max_retries = 5

    def generate_authorization_token(self) -> str:
        """
        Generates Spotify user authorization token based on client_id and client_secret
        :param client_id: your client id from Spotify api
        :param client_secret: your client secret from Spotfiy api
        :return: your authorization token
        :rtype: str
        """
        url = "https://accounts.spotify.com/api/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, data=payload, headers=headers)
        self.access_token = response.json().get("access_token")
        return response.json().get("access_token")

    def is_authenticated(self):
        """
        Checks if user is authenticated
        """
        return True if self.access_token is not None else False
