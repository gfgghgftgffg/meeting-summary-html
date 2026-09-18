#!/usr/bin/env python3
"""Detect meeting input types and prepare one normalized transcript."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

TRANSCRIBER = Path(__file__).with_name("bailian_meeting_minutes.py")
TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".srt", ".vtt", ".json"}
MEDIA_SUFFIXES = {".aac", ".amr", ".avi", ".flac", ".flv", ".m4a", ".mkv", ".mov", ".mp3", ".mp4", ".mpeg", ".ogg", ".opus", ".wav", ".webm", ".wma", ".wmv"}


def detect_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in TEXT_SUFFIXES:
        return "text"
    if suffix in MEDIA_SUFFIXES:
        return "audio"
    try:
        path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        raise RuntimeError(f"Unsupported input type: {path}") from None
    return "text"


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "utf-16"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Unable to decode text input as UTF-8 or UTF-16: {path}")


def transcribe(path: Path, output_dir: Path, index: int, language: str, api_key_env: str) -> str:
    with tempfile.TemporaryDirectory(prefix="meeting-pipeline-asr-", dir=output_dir) as temp_dir:
        temp_path = Path(temp_dir)
        transcript_name = f"part-{index:03d}.md"
        command = [sys.executable, str(TRANSCRIBER), "--audio", str(path), "--language", language, "--output-dir", str(temp_path), "--transcript-name", transcript_name, "--api-key-env", api_key_env]
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
        if completed.stdout:
            print(completed.stdout, end="", file=sys.stderr)
        if completed.returncode != 0:
            if completed.stderr:
                print(completed.stderr, end="", file=sys.stderr)
            raise subprocess.CalledProcessError(completed.returncode, command)
        result = temp_path / transcript_name
        if not result.is_file():
            raise RuntimeError(f"ASR did not produce a transcript for {path}")
        return result.read_text(encoding="utf-8").strip()


def prepare(inputs: list[Path], output_dir: Path, language: str, api_key_env: str) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    kinds = [detect_kind(path) for path in inputs]
    sections: list[str] = ["# Prepared Meeting Transcript", ""]
    used_bailian = False
    for index, (path, kind) in enumerate(zip(inputs, kinds), start=1):
        if kind == "audio":
            used_bailian = True
            content = transcribe(path, output_dir, index, language, api_key_env)
        else:
            content = read_text(path).strip()
        if not content:
            raise RuntimeError(f"Input is empty: {path}")
        if len(inputs) == 1:
            sections.extend([content, ""])
        else:
            sections.extend([f"## Part {index}: {path.name}", "", content, ""])
    transcript_path = output_dir / "meeting-transcript.md"
    transcript_path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    return {"transcript_path": str(transcript_path), "source_files": [str(path) for path in inputs], "input_kinds": kinds, "used_bailian": used_bailian}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Detect text or audio meeting inputs and prepare a normalized transcript.")
    parser.add_argument("--input", action="append", dest="inputs", required=True, help="Meeting text or audio path. Repeat for multiple files.")
    parser.add_argument("--output-dir", required=True, help="Directory for the prepared transcript.")
    parser.add_argument("--language", default="auto", help="ASR language hints, for example en,zh; use auto for detection.")
    parser.add_argument("--api-key-env", default="DASHSCOPE_API_KEY", help="Environment variable containing the ASR API key.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    inputs = [Path(raw).expanduser().resolve() for raw in args.inputs]
    missing = [str(path) for path in inputs if not path.is_file()]
    if missing:
        raise RuntimeError("Input files not found:\n" + "\n".join(missing))
    output_dir = Path(args.output_dir).expanduser().resolve()
    manifest = prepare(inputs, output_dir, args.language, args.api_key_env)
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
