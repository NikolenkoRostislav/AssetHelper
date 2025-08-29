from app.utils.exceptions import *

class BgRemoveService:
    @staticmethod
    async def remove_bg(image: str):
        return {"detail": f"removed background from {image}" }
