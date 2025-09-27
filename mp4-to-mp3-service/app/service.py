import os
#import asyncio
import tempfile
import subprocess
from io import BytesIO
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from app.exceptions import *

class Mp4ToMp3Service:
    @staticmethod
    async def convert(video: UploadFile):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp_path = tmp.name
            while chunk := await video.read(1024 * 1024):
                tmp.write(chunk)

        cmd = ["ffmpeg", "-i", tmp_path, "-vn", "-f", "mp3", "pipe:1"]
        #process = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  #For some reason create_subprocess_exec doesn't work on windows in this case
        #audio_bytes, _ = await process.communicate()
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        audio_bytes, _ = process.communicate()

        os.remove(tmp_path)

        buffer = BytesIO(audio_bytes)
        buffer.seek(0)

        filename, _ = os.path.splitext(video.filename)
        filename = filename.replace("/", "_")

        return StreamingResponse(buffer, media_type="audio/mp3",
            headers={"Content-Disposition": f'attachment; filename="{filename}.mp3"'}
        )
