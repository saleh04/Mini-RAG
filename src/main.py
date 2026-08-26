from contextlib import asynccontextmanager

from async_pymongo import AsyncClient
from fastapi import FastAPI

from helpers.config import Settings
from routes import base, data


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    app.mongo_conn = AsyncClient(settings.MONGODB_URI)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

    yield
    app.mongo_conn.close()

app = FastAPI(lifespan=lifespan)

                  
app.include_router(base.base_router)
app.include_router(data.data_router)