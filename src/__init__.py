from fastapi import FastAPI
from src.models.info import info, tags_metadata

app = FastAPI(openapi_tags=tags_metadata, title=info["title"],
              description=info["description"], version=info["version"], redoc_url="/")

from .routes import *
