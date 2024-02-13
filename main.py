from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from pydantic import ValidationError

from redis import asyncio as aioredis

from auth.auth import auth_backend

from ref.router import router as ref_router
from auth.router import router as auth_router

from config import settings
from utils.utils import fastapi_users

app = FastAPI(
    title=settings.NAME,
    version='1.0',
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"]
)

app.include_router(auth_router)
app.include_router(ref_router)


@app.exception_handler(ValidationError)
async def validation_exception_error(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors()})
    )


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
