from contextlib import asynccontextmanager

from async_pymongo import AsyncClient # type: ignore
from fastapi import FastAPI

from helpers.config import Settings
from routes import base, data
from stores.llm.LLMProviderFactory import LLMProviderFactory


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings() # type: ignore

    app.mongo_conn = AsyncClient(settings.MONGODB_URI) # type: ignore
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE] # type: ignore

    llm_provider_factory = LLMProviderFactory(settings)

    app.generation_client = llm_provider_factory.create(settings.GENERATION_BACKEND) # type: ignore
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID) 

    app.embedding_client = llm_provider_factory.create(settings.EMBEDDING_BACKEND) # type: ignore
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,
                                              embedding_size=settings.EMBEDDING_MODEL_SIZE)

    yield

    app.mongo_conn.close()

app = FastAPI(lifespan=lifespan)

                  
app.include_router(base.base_router)
app.include_router(data.data_router)