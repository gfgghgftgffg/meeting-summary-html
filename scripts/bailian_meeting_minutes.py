#!/usr/bin/env python3
"""Transcribe one local audio file with Alibaba Cloud Model Studio ASR."""

from __future__ import annotations

import argparse
import http.client
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import timedelta
from pathlib import Path
from typing import Any

API_BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
ASR_MODEL = "qwen-audio-3.0-asr-flash-filetrans"
DEFAULT_API_KEY_ENV = "DASHSCOPE_API_KEY"


def request_json(url: str, api_key: str, method: str = "GET", payload: dict[str, Any] | None = None, extra_headers: dict[str, str] | None = None) -> dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    headers = {"Authorization": f"Bearer {api_key}"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    if extra_headers:
        headers.update(extra_headers)
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Model Studio API returned HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Unable to reach Model Studio API: {error.reason}") from error


def get_upload_policy(api_key: str) -> dict[str, Any]:
    query = urllib.parse.urlencode({"action": "getPolicy", "model": ASR_MODEL})
    response = request_json(f"{API_BASE_URL}/uploads?{query}", api_key)
    try:
        return response["data"]
    except KeyError as error:
        raise RuntimeError(f"Temporary upload policy was not returned: {response}") from error


def multipart_field(boundary: str, name: str, value: str) -> bytes:
    return (f"--{boundary}\r\n" f'Content-Disposition: form-data; name="{name}"\r\n\r\n' f"{value}\r\n").encode("utf-8")


def upload_to_temp_storage(audio_path: Path, policy: dict[str, Any]) -> str:
    object_key = f"{policy['upload_dir']}/{audio_path.name}"
    fields = {
        "OSSAccessKeyId": policy["oss_access_key_id"], "Signature": policy["signature"],
        "policy": policy["policy"], "x-oss-object-acl": policy["x_oss_object_acl"],
        "x-oss-forbid-overwrite": policy["x_oss_forbid_overwrite"], "key": object_key,
        "success_action_status": "200",
    }
    boundary = f"----MeetingPipelineUpload{uuid.uuid4().hex}"
    fields_bytes = b"".join(multipart_field(boundary, name, value) for name, value in fields.items())
    file_header = (f"--{boundary}\r\n" f'Content-Disposition: form-data; name="file"; filename="{audio_path.name}"\r\n' "Content-Type: application/octet-stream\r\n\r\n").encode("utf-8")
    closing = f"\r\n--{boundary}--\r\n".encode("utf-8")
    content_length = len(fields_bytes) + len(file_header) + audio_path.stat().st_size + len(closing)
    upload_url = urllib.parse.urlsplit(policy["upload_host"])
    connection = http.client.HTTPSConnection(upload_url.netloc, timeout=120)
    try:
        connection.putrequest("POST", upload_url.path or "/")
        connection.putheader("Content-Type", f"multipart/form-data; boundary={boundary}")
        connection.putheader("Content-Length", str(content_length))
        connection.endheaders()
        connection.send(fields_bytes)
        connection.send(file_header)
        with audio_path.open("rb") as source:
            while chunk := source.read(1024 * 1024):
                connection.send(chunk)
        connection.send(closing)
        response = connection.getresponse()
        detail = response.read().decode("utf-8", errors="replace")
        if response.status != 200:
            raise RuntimeError(f"Temporary upload failed, HTTP {response.status}: {detail}")
    finally:
        connection.close()
    return f"oss://{object_key}"


def format_time(milliseconds: int | float | None) -> str:
    if milliseconds is None:
        return ""
    return str(timedelta(seconds=int(float(milliseconds) / 1000))).zfill(8)


def transcript_to_markdown(result: dict[str, Any]) -> str:
    lines = ["# Meeting Transcript", ""]
    for channel in result.get("transcripts", []):
        for sentence in channel.get("sentences", []):
            text = str(sentence.get("text", "")).strip()
            if not text:
                continue
            timecode = format_time(sentence.get("begin_time"))
            speaker = sentence.get("speaker_id", "unknown")
            prefix = f"[{timecode}] " if timecode else ""
            lines.append(f"{prefix}Speaker {speaker}: {text}")
            lines.append("")
    if len(lines) == 2:
        lines.append("No sentence-level transcript was returned. Use --save-raw to inspect the raw response.")
    return "\n".join(lines).rstrip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Transcribe a local audio file with Alibaba Cloud Model Studio ASR.")
    parser.add_argument("--audio", required=True, help="Local audio file path.")
    parser.add_argument("--language", default="auto", help="Language hints, for example en,zh; use auto for automatic detection.")
    parser.add_argument("--channel-id", type=int, default=0, help="Audio channel index. Default: 0.")
    parser.add_argument("--no-diarization", action="store_true", help="Disable speaker diarization.")
    parser.add_argument("--speaker-count", type=int, help="Expected speaker count, from 2 to 100.")
    parser.add_argument("--output-dir", default=".", help="Output directory. Default: current directory.")
    parser.add_argument("--transcript-name", default="meeting-transcript.md", help="Markdown output filename.")
    parser.add_argument("--save-raw", action="store_true", help="Also save the raw JSON response.")
    parser.add_argument("--api-key-env", default=DEFAULT_API_KEY_ENV, help=f"Environment variable containing the API key. Default: {DEFAULT_API_KEY_ENV}.")
    parser.add_argument("--poll-interval", type=float, default=5.0, help="Polling interval in seconds. Default: 5.")
    parser.add_argument("--poll-timeout", type=float, default=3600.0, help="Maximum polling time in seconds. Default: 3600.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.channel_id < 0:
        parser.error("--channel-id must be non-negative")
    if args.speaker_count is not None and not 2 <= args.speaker_count <= 100:
        parser.error("--speaker-count must be between 2 and 100")
    if args.speaker_count is not None and args.no_diarization:
        parser.error("--speaker-count requires speaker diarization")
    if Path(args.transcript_name).name != args.transcript_name:
        parser.error("--transcript-name must be a filename, not a path")
    if args.poll_interval <= 0 or args.poll_timeout <= 0:
        parser.error("--poll-interval and --poll-timeout must be positive")

    api_key = os.environ.get(args.api_key_env, "").strip()
    if not api_key:
        print(f"Missing API key. Set the {args.api_key_env} environment variable first.", file=sys.stderr)
        return 2
    audio_path = Path(args.audio).expanduser().resolve()
    if not audio_path.is_file():
        parser.error(f"Audio file does not exist: {audio_path}")
    if audio_path.stat().st_size > 1024 * 1024 * 1024:
        parser.error("Temporary upload accepts files up to 1 GB")

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Uploading {audio_path.name} to temporary storage...")
    audio_url = upload_to_temp_storage(audio_path, get_upload_policy(api_key))
    parameters: dict[str, Any] = {"channel_id": [args.channel_id], "diarization_enabled": not args.no_diarization}
    if args.language.lower() != "auto":
        language_hints = [item.strip() for item in args.language.split(",") if item.strip()]
        if not language_hints or len(language_hints) > 4:
            parser.error("--language accepts auto or one to four comma-separated language codes")
        parameters["language_hints"] = language_hints
    if args.speaker_count is not None:
        parameters["speaker_count"] = args.speaker_count

    task = request_json(f"{API_BASE_URL}/services/audio/asr/transcription", api_key, method="POST", payload={"model": ASR_MODEL, "input": {"file_urls": [audio_url]}, "parameters": parameters}, extra_headers={"X-DashScope-Async": "enable", "X-DashScope-OssResourceResolve": "enable"})
    task_id = task.get("output", {}).get("task_id")
    if not task_id:
        raise RuntimeError(f"ASR task was not created: {task}")
    task_url = f"{API_BASE_URL}/tasks/{task_id}"
    deadline = time.monotonic() + args.poll_timeout
    while True:
        task_result = request_json(task_url, api_key)
        output = task_result.get("output", {})
        status = output.get("task_status", "UNKNOWN")
        print(f"ASR status: {status}")
        if status == "SUCCEEDED":
            break
        if status in {"FAILED", "CANCELED", "UNKNOWN"}:
            raise RuntimeError(f"ASR task failed: {task_result}")
        if time.monotonic() >= deadline:
            raise RuntimeError(f"ASR task timed out after {args.poll_timeout:g} seconds")
        time.sleep(args.poll_interval)

    results = output.get("results", [])
    if not results or not results[0].get("transcription_url"):
        raise RuntimeError(f"ASR task completed without a transcript URL: {task_result}")
    with urllib.request.urlopen(results[0]["transcription_url"], timeout=60) as response:
        raw_transcript = json.load(response)
    transcript_path = output_dir / args.transcript_name
    transcript_path.write_text(transcript_to_markdown(raw_transcript), encoding="utf-8")
    if args.save_raw:
        (output_dir / "meeting-transcript.raw.json").write_text(json.dumps(raw_transcript, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Transcript written to: {transcript_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
