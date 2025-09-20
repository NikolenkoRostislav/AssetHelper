import subprocess
import json
from io import BytesIO
from fastapi.responses import StreamingResponse

class YTDownloadService:
    @staticmethod
    async def yt_download(url: str, type: str = "video") -> StreamingResponse:
        info_cmd = ["yt-dlp", "-j", url] 
        info_process = subprocess.run(info_cmd, capture_output=True, text=True)
        info_json = json.loads(info_process.stdout)
        title = info_json.get("title", "downloaded_file").replace("/", "_")

        download_type = "bestaudio" if type == "audio" else "best"
        cmd = ["yt-dlp", "-f", download_type, "-o", "-", url]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        video_bytes = process.communicate()[0]

        buffer = BytesIO(video_bytes)
        buffer.seek(0)

        media_type = "audio/mp3"if type == "audio" else "video/mp4" 
        filename = f"{title}.mp3" if type == "audio" else f"{title}.mp4"

        return StreamingResponse(
            buffer,
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
