from fastapi import APIRouter, UploadFile
from app.service import Mp4ToMp3Service
from app.exceptions import handle_exceptions

router = APIRouter(prefix="/mp4-to-mp3", tags=["mp4-to-mp3"])

@router.get("/")
async def health_check():
    return {"status": "ok"}

@router.post("/convert")
@handle_exceptions
async def convert(video: UploadFile):
    return await Mp4ToMp3Service.convert(video)
