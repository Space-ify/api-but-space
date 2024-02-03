# STL
import os

# PDM
from dotenv import load_dotenv
from fastapi import FastAPI

# LOCAL
from .routes.EdgeDBRoutes import edgedb_router
from .routes.SpotifyRoutes import spotify_router

load_dotenv(".env")
app = FastAPI()

app.include_router(edgedb_router)
app.include_router(spotify_router)
