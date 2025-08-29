from io import BytesIO
from zipfile import ZipFile
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
from app.utils.exceptions import *

class BgRemoveService:
    @staticmethod
    async def remove_bg(image: UploadFile):
        contents = await image.read()
        try:
            input_image = Image.open(BytesIO(contents))
        except Exception:
            raise InvalidEntryError("Something failed")

        output_image = remove(input_image)

        buffer = BytesIO()
        output_image.save(buffer, format="PNG")
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="image/png", headers={
            "Content-Disposition": 'attachment; filename="updated_image.png"'
        })


    @staticmethod
    async def remove_bgs(images: list[UploadFile]):
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w") as zf:
            for image in images:
                contents = await image.read()
                try:
                    input_image = Image.open(BytesIO(contents))
                except Exception:
                    raise InvalidEntryError("Something failed")

                output_image = remove(input_image)

                img_buffer = BytesIO()
                output_image.save(img_buffer, format="PNG")
                img_buffer.seek(0)

                zf.writestr(image.filename, img_buffer.read())
        zip_buffer.seek(0)
        return StreamingResponse(zip_buffer, media_type="application/zip", headers={
            "Content-Disposition": 'attachment; filename="images.zip"'
        })
