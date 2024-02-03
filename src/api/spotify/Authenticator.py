# STL
import os
import base64

# PDM
import requests


class Authenticator:
    def __init__(
        self, CLIENT_ID: str, CLIENT_SECRET: str, REDIRECT_URI: str, CODE: str
    ) -> None:
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.REDIRECT_URI = REDIRECT_URI
        self.CODE = CODE
        self.secret_code = os.urandom(24)
        self.access_token = None
        self.max_retries = 5

    def generate_authorization_token(self) -> str:
        """ """
        url = "https://accounts.spotify.com/api/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()  # Raise an exception if there's an HTTP error
            self.access_token = response.json().get("access_token")
            return self.access_token
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None

    def is_authenticated(self):
        """
        Checks if user is authenticated
        """
        return True if self.access_token is not None else False

    def __create_auth_url(self):
        scope = "user-read-private user-read-email"

        params = {
            "response_type": "code",
            "client_id": self.CLIENT_ID,
            "scope": scope,
            "redirect_uri": self.REDIRECT_URI,
        }

        auth_url = "https://accounts.spotify.com/authorize?" + "&".join(
            [f"{key}={value}" for key, value in params.items()]
        )

        return auth_url

    def generate_authorization_token(self):
        """Generates Spotify user authorization token based on client_id and client_secret
        :param client_id: your client id from Spotify api
        :param client_secret: your client secret from Spotfiy api
        :return: your authorization token
        :rtype: str
        """

        token_url = "https://accounts.spotify.com/api/token"
        code = self.CODE

        auth_header = (
            "Basic "
            + base64.b64encode(
                f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode()
            ).decode()
        )
        data = {
            "code": code,
            "redirect_uri": self.REDIRECT_URI,
            "grant_type": "client_credentials",
        }
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "Authorization": auth_header,
        }

        response = requests.post(token_url, data=data, headers=headers)
        token_info = response.json()
        print(token_info)

        # You can now use token_info to access the access token and other details
        access_token = token_info["access_token"]
        self.access_token = access_token
