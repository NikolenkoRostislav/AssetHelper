import os
import subprocess
from io import BytesIO
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from app.exceptions import *

class Mp4ToMp3Service:
    @staticmethod
    async def convert(video: UploadFile):
        cmd = ["ffmpeg", "-i", "pipe:0", "-f", "mp3", "pipe:1"]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        audio_bytes = process.communicate(input=video.file.read())[0]

        buffer = BytesIO(audio_bytes)
        buffer.seek(0)

        filename, _ = os.path.splitext(video.filename)
        filename = filename.replace("/", "_")

        return StreamingResponse(buffer, media_type=f"audio/mp3",
            headers={"Content-Disposition": f'attachment; filename="{filename}.mp3"'}
        )
