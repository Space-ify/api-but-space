# STL
import os

# PDM
import dotenv

dotenv.load_dotenv(".env")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
CODE = os.getenv("CODE")
BASE_URL = "https://api.spotify.com/v1"
