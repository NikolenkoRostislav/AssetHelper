import os
from io import BytesIO
from zipfile import ZipFile
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
from app.exceptions import *

async def _get_removed_bg_buffer(image: UploadFile):
    try:
        contents = await image.read()
        input_image = Image.open(BytesIO(contents))

        output_image = remove(
            input_image, 
            alpha_matting=True, alpha_matting_foreground_threshold=250,alpha_matting_background_threshold=30, alpha_matting_erode_size=5, 
            post_process_mask=True
        )

        buffer = BytesIO()
        output_image.save(buffer, format="PNG")
        buffer.seek(0)
    except Exception:
        return None
    return buffer

async def _unzip_to_uploadfiles(zip_file: UploadFile) -> list[UploadFile]:
    contents = await zip_file.read()
    input_zip = BytesIO(contents)
    upload_files = []

    try:
        with ZipFile(input_zip, "r") as zf:
            for filename in zf.namelist():
                file_data = zf.read(filename)
                upload_files.append(
                    UploadFile(filename=filename, file=BytesIO(file_data))
                )
    except Exception:
        raise InvalidEntryError("Failed to process the zip file.")

    return upload_files

class BgRemoveService:
    @staticmethod
    async def remove_bg(image: UploadFile):
        buffer = await _get_removed_bg_buffer(image)
        if buffer is None:
            raise InvalidEntryError("Failed to process the image.")

        filename, _ = os.path.splitext(image.filename)
        return StreamingResponse(buffer, media_type="image/png", headers={
            "Content-Disposition": f'attachment; filename="{filename}.png"'
        })

    @staticmethod
    async def remove_bgs(images: list[UploadFile]):
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w") as zf:
            for image in images:
                buffer = await _get_removed_bg_buffer(image)
                if buffer is None:
                    raise InvalidEntryError("Failed to process the image.")
                zf.writestr(image.filename, buffer.read())
        zip_buffer.seek(0)
        return StreamingResponse(zip_buffer, media_type="application/zip", headers={
            "Content-Disposition": 'attachment; filename="images.zip"'
        })

    @staticmethod
    async def remove_bgs_zip(zip_file: UploadFile):
        upload_files = await _unzip_to_uploadfiles(zip_file)
        return await BgRemoveService.remove_bgs(upload_files)