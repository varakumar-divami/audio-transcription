import os
import yt_dlp


def download_audio(url: str, output_dir: str = "recordings") -> tuple[str, str]:
    """Download audio from YouTube URL. Returns (audio_path, video_title)."""
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(id)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": False,
        "no_warnings": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info.get("id", "audio")
        title = info.get("title", video_id)
        audio_path = os.path.join(output_dir, f"{video_id}.mp3")
        return audio_path, title
