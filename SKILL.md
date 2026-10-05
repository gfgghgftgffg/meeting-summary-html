---
name: meeting-summary-html
disable-model-invocation: true
description: Create a grounded, self-contained HTML meeting brief from a transcript, text file, or local audio/video input. Detect the input type first and call Alibaba Cloud ASR only when media must be transcribed.
---

# Meeting Summary HTML

This skill accepts an existing transcript or local media and produces a complete, readable, self-contained HTML meeting brief. It is designed to work as a host-neutral workflow in Pi, Codex, Claude, or another agent environment.

## Current-Host Contract

- The invoking agent reads the transcript, performs the analysis, and authors the HTML in its current session using the host's native available read, shell, and write tools. The helper does not generate the brief.
- Do not start `codex exec`, `claude`, `pi`, or any other external agent/LLM CLI; do not hard-code a text-summary model or provider, or detect environment variables to reconstruct a parent session/provider. Keep the current host's session and routing.
- The skill does not initiate delegation. Delegate only when explicitly authorized by the user's host policy, using that host's native tools and routing.
- If required read/shell/write capabilities or a Python interpreter are unavailable, report the concrete blocker. Never silently switch hosts or bypass permissions. Manual invocation remains deliberate (`disable-model-invocation: true`).

## Path Resolution

Use the directory containing **this loaded SKILL.md** as `<skill-directory>`. Resolve every bundled script, reference, and example from that directory, never from the shell working directory or a hard-coded Desktop, `.codex`, or `.pi` location. Resolve user-supplied input and output paths against the invoking session's working directory before any optional directory change.

Choose the user's requested output directory; if none is supplied, use a suitable directory beside the input in the user's workspace, never an installation-directory default. Commands below show placeholders: substitute quoted absolute paths and a selected available Python interpreter (`python3` where appropriate); these are not literal runtime interpolation.

## Input Routing

1. Inspect the supplied input path or paths before summarizing.
2. Treat Markdown, plain text, SRT, VTT, and JSON transcript files as text. Read them directly and do not call Alibaba Cloud ASR.
3. Treat supported audio and video files as media. Run the bundled `scripts/prepare_meeting_input.py` via its resolved absolute path so only media inputs are sent to ASR.
4. Mixed input lists are allowed. Preserve source order and transcribe only media files.
5. Never upload a text transcript to the ASR provider. Text-only input does not require an API key.

## Prepare the Transcript

Run the bundled helper with the selected available Python interpreter when transcript preparation is needed (text may also be read directly):

~~~text
"<python-interpreter>" "<skill-directory>/scripts/prepare_meeting_input.py" --input "<absolute-input-path>" --output-dir "<absolute-user-output-directory>"
~~~

Use the host's shell syntax for a quoted executable (for example, PowerShell requires `&` before it). Repeat --input for multiple files. The helper prints a JSON manifest containing transcript_path, source_files, input_kinds, and used_bailian.

Python prepares transcripts only. Its sole existing subprocess uses `sys.executable` (the selected Python interpreter) to run the bundled `bailian_meeting_minutes.py` for media ASR. The only fixed model is `qwen-audio-3.0-asr-flash-filetrans`, an ASR model, not a text-summary model. There is no external agent CLI or text-generation API call in these helpers.

For media input, the helper reads the environment variable named by --api-key-env, defaulting to DASHSCOPE_API_KEY. The key must never be written into source files, manifests, logs, generated HTML, or commits.

After the helper finishes, read the complete transcript at transcript_path. Use the host's read offsets or chronological chunks until the entire file has been read; Pi's read tool can truncate output. A truncated first read is not the complete transcript.

## Generate the HTML Brief

Read [references/summary-meeting-html.md](references/summary-meeting-html.md) before drafting. It contains the full long-form HTML requirements from the original meeting-summary-html skill.

Write the final HTML in the chosen user output directory, beside the prepared transcript unless the user specifies another location; never default to the skill installation directory. Keep the generated HTML self-contained: inline CSS, no CDN, no external font, no network request, and no required JavaScript package.

Preserve the source language unless the user requests a different output language. The HTML brief must include the required overview, chapter scan, detailed discussion, speaker summaries, viewpoint tree, and closing recap.

## Grounding and Privacy

- Read the entire transcript before writing the brief.
- Preserve timestamps, speaker names, uncertainty, and source language.
- Keep confirmed outcomes separate from proposals, hypotheses, risks, and open questions.
- Do not invent owners, dates, decisions, experiments, or causal claims.
- Tell the user when media was uploaded to Alibaba Cloud temporary storage for transcription.
- Revoke any API key that has ever been exposed in source code or chat history.
