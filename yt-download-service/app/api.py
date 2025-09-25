from fastapi import APIRouter, UploadFile
from app.service import YTDownloadService
from app.exceptions import handle_exceptions

router = APIRouter(prefix="/yt-download", tags=["yt-download"])

@router.get("/")
async def health_check():
    return {"status": "ok"}

@router.get("/video")
@handle_exceptions
async def download_video(url: str):
    return await YTDownloadService.yt_download(url, type="video")

@router.get("/audio")
@handle_exceptions
async def download_audio(url: str):
    return await YTDownloadService.yt_download(url, type="audio")
