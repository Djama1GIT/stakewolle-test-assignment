from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/")
async def index():
    return JSONResponse(content={}, status_code=200)
