# Meeting Summary HTML

A host-neutral skill for turning a meeting transcript, text file, or local audio/video file into a grounded, self-contained HTML meeting brief. It works with Codex, Claude, or another agent that can execute a local Python helper.

## What It Does

The skill routes inputs automatically:

1. Text-like inputs are read directly. No ASR call is made.
2. Audio and video inputs are sent to Alibaba Cloud Model Studio only when transcription is needed.
3. Mixed input lists are supported; only media files are transcribed.
4. The prepared transcript is passed through the original long-form HTML meeting-summary workflow.

This means users do not need to operate a separate CLI or manually decide whether Bailian is required. The CLI-compatible Python files remain as implementation helpers, but the main interface is the skill workflow.

## Supported Inputs

Text-like files:

- Markdown
- Plain text
- SRT subtitles
- VTT subtitles
- JSON transcripts

Media files:

- AAC, AMR, AVI, FLAC, FLV
- M4A, MKV, MOV, MP3, MP4, MPEG
- OGG, OPUS, WAV, WEBM, WMA, WMV

## Workflow

The skill first runs the bundled preparation helper:

~~~text
python scripts/prepare_meeting_input.py --input <path> --output-dir <work-directory>
~~~

Use python3 on macOS or Linux when needed. Repeat --input for multiple files. The helper prints a JSON manifest with the normalized transcript path, source files, detected input kinds, and whether Alibaba Cloud ASR was used.

The agent then reads the complete transcript and generates the HTML brief using the bundled reference at references/summary-meeting-html.md. The original visual reference is preserved at references/transcript-summary-sketch.html.

## Generated Brief Structure

The HTML output contains:

- Header and meeting metadata
- Full-meeting overview
- Chapter-at-a-glance
- Theme-based deep dive
- Speaker summaries
- Viewpoint tree
- Closing recap with confirmed outcomes, action items, risks, and unresolved questions

It also preserves timestamp anchors, mobile fallback, print styles, source grounding, and the distinction between confirmed and unconfirmed content.

## Authentication

Only media input requires an Alibaba Cloud Model Studio API key. Store it in an environment variable and never commit it:

macOS/Linux:

~~~sh
export DASHSCOPE_API_KEY="your-api-key"
~~~

Windows PowerShell:

~~~powershell
$env:DASHSCOPE_API_KEY = "your-api-key"
~~~

Use --api-key-env to select another variable name. Text-only inputs do not require this variable.

## Privacy

Audio and video files are uploaded to Alibaba Cloud temporary storage for ASR. Check the provider retention and processing terms before using this skill with sensitive meetings. Text-only inputs remain local during preparation. Revoke any API key that has ever been exposed in source code or chat history.

## Development

The deterministic helper uses Python standard-library modules and is cross-platform. Run the offline tests with:

~~~sh
python -m unittest discover -s tests -v
~~~

The example page can be opened directly as index.html.

## Repository Layout

~~~text
.
|-- SKILL.md
|-- agents/openai.yaml
|-- scripts/
|   |-- prepare_meeting_input.py
|   `-- bailian_meeting_minutes.py
|-- references/
|   |-- summary-meeting-html.md
|   `-- transcript-summary-sketch.html
|-- examples/transcript-summary-sketch.html
|-- docs/preview.png
`-- index.html
~~~

## License

MIT.
