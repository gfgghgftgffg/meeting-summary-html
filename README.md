# Meeting Summary HTML

A Codex skill for turning complete meeting transcripts in any language into grounded, readable, self-contained HTML meeting briefs.

The skill preserves the depth of the source while making the meeting easy to read at three levels: a quick overview, a structured scan, and a detailed research read.

## Preview

This is the actual rendered preview of the example HTML included in this repository:

![Meeting Summary HTML example preview](docs/preview.png)

Open the full example here:

- [Example HTML](examples/transcript-summary-sketch.html)
- [Project entry page](index.html)

## What It Produces

Each generated brief uses the source transcript as its grounding and keeps confirmed outcomes separate from proposals, hypotheses, risks, and unresolved questions.

### 1. Header and Meeting Metadata

The document opens with the meeting topic, date, duration, participants, and other source-grounded metadata.

### 2. Full-Meeting Overview

A concise narrative explains the meeting purpose, the main reasoning arc, the current state, and the most consequential next steps.

### 3. Chapter-at-a-Glance

A chronological scan lists every major chapter with start and end timestamps, a conclusion-oriented title, and a substantive preview of the discussion and its outcome.

### 4. Theme-Based Deep Dive

The detailed analysis groups the conversation by theme rather than merely repeating the transcript. Each substantial theme can cover:

- context and the underlying problem;
- positions, arguments, disagreement, and reasoning;
- evidence, examples, and timestamp anchors;
- current conclusion, validation status, and unresolved questions.

### 5. Speaker Summaries

The brief preserves meaningful differences between speakers, including their roles, evidence, changes of view, commitments, and attributable follow-up. Empty or unsupported fields are omitted.

### 6. Viewpoint Tree

An accessible native HTML and CSS tree maps the meeting's central question or workstream to its main positions, confirmed facts, proposals, constraints, risks, consequences, and open questions.

### 7. Closing Recap

The final section brings together confirmed outcomes, action items, owners and dates when grounded, risks or disagreements, and unresolved questions. Actions are presented in a readable table with a mobile fallback.

## Design and Delivery

- Works with transcripts in any language; the output language follows the source and task context.
- Self-contained HTML with inline CSS and no server, CDN, external font, image, JavaScript package, or network request.
- Responsive layout for desktop and mobile reading.
- Print-friendly styles for archival or PDF output.
- Timestamp anchors and semantic headings support navigation and source verification.
- Visual signposts clarify structure without replacing the underlying discussion.

## Usage

After installing this repository as a Codex skill, use:

```text
Use $summary-meeting-html to turn this transcript into a readable, self-contained HTML meeting brief.
```

The skill generates `<transcript-stem>-summary.html` and requires complete chronological coverage of the meeting, grounded action ownership and dates, and a clear distinction between confirmed and unconfirmed content.

## Repository Layout

```text
.
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- examples/
|   `-- transcript-summary-sketch.html
|-- docs/
|   `-- preview.png
`-- index.html
```

## Note

The people, dates, numbers, and conclusions in the example page are fictional and are included only to demonstrate the structure and visual treatment.
