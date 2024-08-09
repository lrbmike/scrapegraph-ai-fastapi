from fastapi import FastAPI

from app.routers import crawl

import sys
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

sys.path.append(os.path.join(os.path.dirname(__file__)))

app = FastAPI()

app.include_router(crawl.router)