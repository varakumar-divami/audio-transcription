# YouTube Audio Transcriber

Download audio from a YouTube video and transcribe it to English text.
Supports English and Telugu audio.

## Requirements

- macOS with [Homebrew](https://brew.sh)
- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (`brew install uv`)

## Setup

Run once to install all dependencies:

```bash
bash setup.sh
```

This installs:
- `ffmpeg` (via Homebrew)
- `yt-dlp` — YouTube audio downloader
- `openai-whisper` — transcription engine

## Usage

```bash
source .venv/bin/activate
python transcribe.py <youtube-url>
```

**Example:**

```bash
python transcribe.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Output files saved in the current directory:
- `<video-title>.mp3` — downloaded audio
- `<video-title>.txt` — English transcript

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `small` | Whisper model size |
| `--output-dir` | `.` | Directory to save audio and transcript |

```bash
python transcribe.py <url> --model medium --output-dir ./output
```

## Model Size Guide

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | 75MB | fastest | low |
| base | 142MB | fast | moderate |
| small | 461MB | fast | good |
| medium | 1.4GB | moderate | better |
| large | 2.9GB | slow | best |

To change the default model, edit line 17 in `transcribe.py`:

```python
DEFAULT_MODEL = "medium"
```

## Notes

- Telugu audio is automatically translated to English (not just transcribed).
- First run downloads the Whisper model weights — may take a few minutes depending on model size.
