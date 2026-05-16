import os
import time
from faster_whisper import WhisperModel

DEFAULT_MODEL = "small"


def transcribe_to_english(audio_path: str, model_name: str = DEFAULT_MODEL, on_segment=None) -> str:
    """Load Whisper model and transcribe audio to English. Always outputs English.

    on_segment: optional callback(start, end, text) called for each decoded segment.
    """
    t0 = time.time()
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    print(f"    Model loaded in {time.time() - t0:.1f}s", flush=True)

    segments, info = model.transcribe(audio_path, task="translate")
    print(f"    Detected language: {info.language} (confidence: {info.language_probability:.0%})")
    print("    Transcribing — segments will appear in real time:\n")

    parts = []
    for segment in segments:
        text = segment.text.strip()
        print(f"    [{segment.start:6.1f}s -> {segment.end:6.1f}s]  {text}", flush=True)
        if on_segment:
            on_segment(segment.start, segment.end, text)
        parts.append(text)

    return "\n".join(parts)


def save_transcript(text: str, title: str, output_dir: str = "outputs") -> str:
    """Save transcript to outputs dir. Returns the file path."""
    os.makedirs(output_dir, exist_ok=True)
    safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
    out_path = os.path.join(output_dir, f"{safe_title}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    return out_path
