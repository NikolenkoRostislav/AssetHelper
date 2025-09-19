from fastapi import APIRouter, UploadFile
from app.service import BgRemoveService
from app.utils.exceptions import handle_exceptions

router = APIRouter(prefix="/bg-rm", tags=["bg-rm"])

@router.post("/image")
@handle_exceptions
async def bg_rm(image: UploadFile):
    return await BgRemoveService.remove_bg(image)

@router.post("/images")
@handle_exceptions
async def bg_rm(images: list[UploadFile]):
    return await BgRemoveService.remove_bgs(images)

@router.post("/test")
async def test():
    #contents = await image.read()
    return {"test": "ok"}  