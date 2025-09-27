import os
import tempfile
import subprocess
from io import BytesIO
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from app.exceptions import *

class Mp4ToMp3Service:
    @staticmethod
    async def convert(video: UploadFile):
        tmp_path = os.path.join(tempfile.gettempdir(), f"tmp_{video.filename}")
        with open(tmp_path, "wb") as f:
            f.write(await video.read())

        cmd = ["ffmpeg", "-i", tmp_path, "-vn", "-f", "mp3", "pipe:1"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        audio_bytes = process.communicate()[0]

        os.remove(tmp_path)

        buffer = BytesIO(audio_bytes)
        buffer.seek(0)

        filename, _ = os.path.splitext(video.filename)
        filename = filename.replace("/", "_")

        return StreamingResponse(buffer, media_type="audio/mp3",
            headers={"Content-Disposition": f'attachment; filename="{filename}.mp3"'}
        )
