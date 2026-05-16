#!/usr/bin/env python3
"""
transcribe.py — CLI for YouTube audio transcription.
Downloads audio and transcribes to English (supports English and Telugu).

Usage:
    python transcribe.py <youtube-url> [--model small] [--output-dir outputs]
"""

import argparse
import os
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "0"

from transcriber import download_audio, transcribe_to_english, save_transcript, DEFAULT_MODEL


def step(n: int, total: int, msg: str):
    print(f"\n[{n}/{total}] {msg}", flush=True)


def main():
    parser = argparse.ArgumentParser(description="YouTube audio transcriber (English/Telugu -> English)")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: small)",
    )
    parser.add_argument("--output-dir", default="outputs", help="Directory to save transcripts")
    parser.add_argument("--recordings-dir", default="recordings", help="Directory to save audio files")
    args = parser.parse_args()

    total = 4

    step(1, total, "Downloading audio from YouTube...")
    audio_path, title = download_audio(args.url, args.recordings_dir)
    print(f"    Saved: {audio_path}")

    step(2, total, f"Loading Whisper model '{args.model}'...")
    transcript = transcribe_to_english(audio_path, args.model)

    step(3, total, "Saving transcript...")
    txt_path = save_transcript(transcript, title, args.output_dir)
    print(f"    Saved: {txt_path}")

    step(4, total, "Done.")
    print("\n--- Transcript Preview (first 500 chars) ---")
    print(transcript[:500])


if __name__ == "__main__":
    main()
