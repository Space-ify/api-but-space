# STL
import os

# PDM
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# LOCAL
from .routes.EdgeDBRoutes import edgedb_router
from .routes.SpotifyRoutes import spotify_router

load_dotenv(".env")
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(edgedb_router)
app.include_router(spotify_router)
