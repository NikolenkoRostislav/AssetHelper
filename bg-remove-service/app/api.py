from fastapi import APIRouter
from app.service import BgRemoveService
from app.utils.exceptions import handle_exceptions

router = APIRouter(prefix="/bg-rm", tags=["bg-rm"])

@router.post("/")
@handle_exceptions
async def bg_rm(image: str):
    return await BgRemoveService.remove_bg(image)
