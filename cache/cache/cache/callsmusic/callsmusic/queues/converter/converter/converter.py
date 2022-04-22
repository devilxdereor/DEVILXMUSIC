from os import path
import asyncio

from helpers.errors import FFmpegReturnCodeError


async def convert(file_path: str) -> str:
    out = path.basename(file_path)
    out = out.split(".")
    out[-1] = "raw"
    out = ".".join(out)
    out = path.basename(out)
    out = path.join("raw_files", out)

    if path.isfile(out):
        return out

proc = await asyncio.create_subprocess_shell(
        f"ffmpeg -y -i {file_path} -f s16le -ac 1 -ar 48000 -acodec pcm_s16le {out}",
        asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    await proc.communicate()

    if proc.returncode != 0:
        raise FFmpegReturnCodeError("FFmpeg did not return 0")

    return out

downloaders/__init__.py

from os import path

from yt_dlp import YoutubeDL

from config import BOT_NAME as bn, DURATION_LIMIT
from helpers.errors import DurationLimitError

ydl_opts = {
    "format": "bestaudio/best",
    "verbose": True,
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"❌ Videos longer than {DURATION_LIMIT} minute(s) aren't allowed, the provided video is {duration} minute(s)"
        )

    ydl.download([url])
    return path.join("downloads", f"{info['id']}.{info['ext']}")

