#!/usr/bin/env bash
set -e

echo "==> Checking ffmpeg..."
if ! command -v ffmpeg &>/dev/null; then
  echo "    Installing ffmpeg via Homebrew..."
  brew install ffmpeg
else
  echo "    ffmpeg already installed."
fi

echo "==> Setting up Python venv..."
if [ ! -d ".venv" ]; then
  uv venv .venv
fi

echo "==> Installing Python dependencies..."
uv pip install --python .venv/bin/python yt-dlp faster-whisper tqdm fastapi uvicorn python-multipart

echo ""
echo "Setup complete. Usage:"
echo "  source .venv/bin/activate"
echo "  python transcribe.py <youtube-url>"
