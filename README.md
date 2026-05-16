# Audio Transcriber

Transcribe YouTube videos and live voice recordings to English text.
Supports English and Telugu audio via OpenAI Whisper.

## Requirements

- macOS with [Homebrew](https://brew.sh)
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (`brew install uv`)
- ffmpeg (`brew install ffmpeg`)

## Setup

```bash
bash setup.sh
```

Installs: `ffmpeg`, `yt-dlp`, `faster-whisper`, `fastapi`, `uvicorn`, `tqdm`

## Project Structure

```
audio-transription/
├── transcriber/         # core module
│   ├── __init__.py
│   ├── downloader.py    # YouTube audio download
│   └── transcriber.py  # Whisper transcription
├── recordings/          # audio files — gitignored
├── outputs/             # transcripts saved here
├── static/
│   └── index.html       # web UI
├── server.py            # FastAPI backend
├── transcribe.py        # CLI entry point
├── setup.sh
└── docs/
    └── ROADMAP.md
```

## Usage

### Web UI

```bash
source .venv/bin/activate
uvicorn server:app --reload
```

Open `http://localhost:8000`

**YouTube tab** — paste a URL, pick model size, click Transcribe. Live segments stream in as Whisper decodes. Transcript and download link appear on completion.

**Record Voice tab** — click the mic button to start recording, click again to stop. Audio is sent to the backend automatically and transcribed using the same pipeline.

### CLI

```bash
source .venv/bin/activate
python transcribe.py <youtube-url>
```

Options:

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `small` | Whisper model size |
| `--output-dir` | `outputs` | Directory for transcripts |
| `--recordings-dir` | `recordings` | Directory for audio files |

## Model Size Guide

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | 75MB | fastest | low |
| base | 142MB | fast | moderate |
| small | 461MB | fast | good |
| medium | 1.4GB | moderate | better |
| large | 2.9GB | slow | best |

Default is `small`. To change it, edit `transcriber/transcriber.py`:

```python
DEFAULT_MODEL = "medium"
```

## Notes

- Telugu audio is automatically translated to English.
- First run downloads Whisper model weights — one-time download per model size.
- Audio files are saved to `recordings/` and excluded from git.
- Transcripts are saved to `outputs/` as `.txt` files, one line per segment.
