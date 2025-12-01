from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import opcua_router
from contextlib import asynccontextmanager
from db.db_actions import init_models
from core.config import ALLOWED_ORIGINS
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Lifespan context manager to handle startup and shutdown events.'''
    await init_models()
    yield

def create_app() -> FastAPI:
    '''Create and configure the FastAPI application.'''
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,  # Needed for cookies/auth headers
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],  # Specific headers
    )

    app.include_router(opcua_router.router, tags=["OPC UA Web Access API"], prefix="/opcua")

    return app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8000)