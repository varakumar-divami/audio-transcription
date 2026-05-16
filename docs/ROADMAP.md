# Roadmap — Audio Transcriber

## Feature 1 — CLI Transcription Tool
**Status:** Done

- Download audio from any YouTube URL via `yt-dlp`
- Transcribe English and Telugu audio to English text using `faster-whisper`
- Real-time segment output with timestamps in the terminal
- Configurable Whisper model size (tiny → large)
- Audio saved to `recordings/` (gitignored), transcripts saved to `outputs/`

---

## Feature 2 — Web UI (YouTube)
**Status:** Done

- Web page that accepts a YouTube URL and model size
- Transcription runs in a background thread — UI stays responsive
- Step indicators: Downloading → Transcribing → Saving → Done
- Live segments stream into the page as Whisper decodes them
- Transcript displayed on completion with Download and Copy actions
- Past transcripts listed and downloadable from the same page

---

## Feature 3 — Live Voice Recording
**Status:** Done

- Record mic audio directly in the browser via MediaRecorder API
- Live timer while recording; click mic again to stop
- Audio sent to the backend on stop, saved to `recordings/`
- Same Whisper transcription pipeline and segment streaming as YouTube flow
- Transcript and download link shown on completion
- Output saved to `outputs/` as `voice_recording_<timestamp>.txt`

---
