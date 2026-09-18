---
name: meeting-summary-html
description: Create a grounded, self-contained HTML meeting brief from a transcript, text file, or local audio/video input. Detect the input type first and call Alibaba Cloud ASR only when media must be transcribed.
---

# Meeting Summary HTML

This skill accepts an existing transcript or local media and produces a complete, readable, self-contained HTML meeting brief. It is designed to work as a host-neutral workflow in Codex, Claude, or another agent environment.

## Input Routing

1. Inspect the supplied input path or paths before summarizing.
2. Treat Markdown, plain text, SRT, VTT, and JSON transcript files as text. Read them directly and do not call Alibaba Cloud ASR.
3. Treat supported audio and video files as media. Run scripts/prepare_meeting_input.py so only media inputs are sent to ASR.
4. Mixed input lists are allowed. Preserve source order and transcribe only media files.
5. Never upload a text transcript to the ASR provider. Text-only input does not require an API key.

## Prepare the Transcript

Run the bundled helper with the available Python interpreter:

~~~text
python scripts/prepare_meeting_input.py --input <path> --output-dir <work-directory>
~~~

Use python3 on macOS or Linux when that is the available command. Repeat --input for multiple files. The helper prints a JSON manifest containing transcript_path, source_files, input_kinds, and used_bailian.

For media input, the helper reads the environment variable named by --api-key-env, defaulting to DASHSCOPE_API_KEY. The key must never be written into source files, manifests, logs, generated HTML, or commits.

After the helper finishes, read the complete transcript at transcript_path.

## Generate the HTML Brief

Read [references/summary-meeting-html.md](references/summary-meeting-html.md) before drafting. It contains the full long-form HTML requirements from the original meeting-summary-html skill. Use [references/transcript-summary-sketch.html](references/transcript-summary-sketch.html) as the visual and structural reference.

Write the final HTML beside the prepared transcript unless the user specifies another location. Keep the generated HTML self-contained: inline CSS, no CDN, no external font, no network request, and no required JavaScript package.

Preserve the source language unless the user requests a different output language. The HTML brief must include the required overview, chapter scan, detailed discussion, speaker summaries, viewpoint tree, and closing recap.

## Grounding and Privacy

- Read the entire transcript before writing the brief.
- Preserve timestamps, speaker names, uncertainty, and source language.
- Keep confirmed outcomes separate from proposals, hypotheses, risks, and open questions.
- Do not invent owners, dates, decisions, experiments, or causal claims.
- Tell the user when media was uploaded to Alibaba Cloud temporary storage for transcription.
- Revoke any API key that has ever been exposed in source code or chat history.
