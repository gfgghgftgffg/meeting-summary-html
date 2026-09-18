---
name: summary-meeting-html
description: "Create a complete, grounded Chinese meeting brief as a polished self-contained HTML reading document. Use for transcripts when full detail must remain readable and visually structured, not merely summarized in Markdown."
---

# Summary Meeting HTML

Create a self-contained HTML meeting brief that is pleasant to read for a human, while preserving the analytical depth of a detailed meeting summary. This is a document deliverable, not a landing page or a dashboard.

The brief must work at three reading depths: a one-minute reader can rely on the overview and concise status index; a scanning reader can use the chapter overview; and a research reader can follow the detailed discussion, speaker positions, and recap without returning to the transcript.

## Grounding

- Read the complete supplied transcript before drafting. Preserve speaker names, timestamps, and uncertainty.
- For transcripts longer than 20 minutes or 12,000 characters, read chronological chunks with explicit boundaries. Use 60-120 seconds of overlap at every boundary; record each chunk's first and last timestamp and note any topic that continues across it.
- Synthesize chapters by topic, decision, experiment, or shift in reasoning. A read boundary is never by itself a chapter boundary. Resolve overlap before writing so an argument is not split or repeated.
- Before delivery, identify the source's final timestamp and verify that the final chronological chapter reaches it. Do not state a shorter meeting duration because a read was truncated.
- Do not fabricate decisions, owners, deadlines, experiments, or causal claims. Clearly distinguish confirmed outcomes from proposals, hypotheses, and unresolved questions.

## Detail Mode

Use detailed mode by default for transcripts longer than 20 minutes. In this mode, retain the reasoning path for each substantive theme: its context, competing positions, evidence or examples, disagreement, current status, and unresolved questions. Add timestamp anchors for consequential claims, proposals, and commitments.

Do not make a long meeting a flat list or a chronological transcript rewrite. Form semantic chapters first, then synthesize across them. Do not pad with restated conclusions.

## Deliverable

Write `<transcript-stem>-summary.html` next to the input transcript. Use UTF-8 and include all CSS in the file. The document must work by opening it directly in a browser: no server, CDN, external font, image, JavaScript package, or network request.

Use [examples/transcript-summary-sketch.html](examples/transcript-summary-sketch.html) as a visual and structural reference. Read it before writing output. Reuse its successful long-form patterns where appropriate: the header, status index, navigation, chapter scan, argument tree, action table, mobile fallback, and print styles. It is an example, not a locked template: adapt composition, visual annotations, and local components to make the meeting's reasoning easier to understand.

Keep the complete meeting structure, in this order. When a supplied Markdown brief already has a fuller structure, preserve its substantive sections and subheadings rather than compressing them into fewer HTML sections:

1. A header with topic, date, duration, and participants.
2. A full-meeting overview (`全文概要`) that explains the meeting purpose, reasoning arc, present state, and consequential next steps in 3-6 short paragraphs.
3. A chapter-at-a-glance section (`章节速览`) with start and end timestamps, specific conclusion-oriented titles, and a substantive preview of every major chronological chapter.
4. A theme-based deep dive (`会议内容总结`) covering context, arguments, evidence, current status, and timestamp anchors.
5. Speaker summaries (`发言总结`) that preserve meaningful differences in position, change of view, and commitments.
6. A discussion/argument tree (`观点树`) showing relationships among confirmed facts, proposals, risks, and open questions. Render it as accessible native HTML and CSS rather than requiring Mermaid or external JavaScript.
7. A closing recap (`要点回顾`) containing confirmed outcomes, action items, risks, and unresolved questions.

Use the source Markdown brief as the content and hierarchy baseline when one exists beside the transcript. Preserve its required headings, chapter coverage, and meaningful subheadings in the HTML. Do not summarize a detailed Markdown brief a second time during conversion.

Do not replace detailed material with executive summaries, cards, or visual decoration. Visual elements are signposts to the full content, never substitutes for it.

## Reading Design

Build a quiet, polished editorial reading layout rather than a product dashboard. The default art direction is **手绘工作坊笔记 / Pastel Sketchbook Brief**: a research-notebook brief that feels light and handmade while remaining precise and highly readable.

- Use a warm-white paper surface, hand-drawn dark outlines, pastel blue, mint, lavender, and peach blocks, plus orange for cautions or unresolved risk. Maintain high contrast and keep body text in a clean sans-serif font with stable line height.
- Make the title centered and prominent. Use circular section numbers. Treat the overview, status index, and chapter scan as irregular rounded note cards; use spacious outlined blocks for deep reasoning.
- Allow a small amount of rotation, dashed rules, arrows, connectors, and simple shadows when they clarify a process, comparison, relationship, or movement of reasoning. Do not use them as generic decoration.
- Preserve the six primary reading sections and the reference template's responsive long-form patterns, but freely adapt navigation, page composition, visual annotations, and local components to the actual meeting content.
- Make the title area visually distinct with a neutral document label, a restrained topic title, and a concise metadata line. Do not invent a brand, logo, image, or slogan.
- Place a source-grounded key take and a concise index of `已确认`, `待验证`, and `待决` near the opening. Each value must remain grounded and concise.
- Establish hierarchy through the type scale, sketchbook cards, rhythm, and section signposts. Avoid dense component mosaics; individual chapter items, cautions, tree nodes, and actions may receive local emphasis when useful.
- Make timestamps small but high contrast. Use them as visual anchors beside or above chapter titles without making a timeline that dominates the prose.
- Keep the theme deep dives in natural prose with short labeled subheads such as `问题`, `讨论`, `当前落点`, and `依据`. Do not force every section into identical boxed widgets.
- Render action items as a readable table with a stacked mobile fallback. Use semantic HTML (`header`, `nav`, `main`, `section`, `article`, `aside`, `table`) and accessible headings.
- Avoid gradients, glassmorphism, corporate-dashboard styling, overly realistic illustration, dense component mosaics, emoji, bokeh/orbs, and fabricated logos. On mobile, collapse grids and note cards to one column.
- Do not reduce rich source content to a bare title-plus-paragraph treatment. Each major section needs a clear visual entry point and its source-grounded subtopics remain visibly distinct.

For the detailed discussion, visibly distinguish the reasoning fields `背景与问题`, `讨论与论证`, `当前结论`, and `依据锚点` when the source supports them. For speaker summaries, include only meaningful differences in role, evidence, changed view, commitments, and attributable follow-up; omit empty fields.

## CSS Baseline

Use the CSS architecture and responsive safeguards in the reference template as a starting point, then adapt its tokens and components to the sketchbook direction and source content. Preserve print readability, linked-section offsets, and reduced-motion handling.

## Content Quality

- In detailed mode, the theme analysis must contain more explanatory substance than the opening narrative.
- Give every substantial chronological chapter a grounded outcome or an explicitly unresolved status.
- Keep speaker summaries asymmetric: include only points, interactions, and commitments attributable to that speaker.
- Use timestamp anchors for consequential claims, proposals, commitments, and disagreements.
- The status strip, discussion map, and action table must not elevate an unverified proposal into a confirmed conclusion.
- The overview, chapter overview, detailed analysis, speaker summary, viewpoint tree, and recap are distinct required reading layers. Do not substitute one for another.
- In detailed mode, each substantial chronological chapter must cover its trigger or context, positions or reasoning, relevant example or evidence, and an outcome or explicit open state. A five-minute-plus discussion must not collapse into a vague single sentence.
- In the recap, put only explicit agreements or results under confirmed outcomes. Put hypotheses, directions, and unvalidated claims under risks, disagreements, and open questions.
- The viewpoint tree root must be the meeting's central question, decision, or workstream. Its first-level branches should be the 2-5 main positions, conclusions, or competing approaches; second-level branches should clarify evidence, constraints, objections, consequences, or hypotheses. Preserve status labels such as confirmed, proposal, disagreement, pending validation, and risk.

## Verification

Before writing, verify that all seven content areas are present, the chapters cover the source in order through its final timestamp, each chapter has an outcome or open state, the action owners and dates are grounded, and the opening narrative agrees with the detailed analysis. In detailed mode, verify that the detailed analysis has more explanatory substance than the overview and retains timestamp anchors.

Inspect the generated HTML as text for correct nesting, working internal anchor targets, preserved heading hierarchy, and a mobile media query. If browser tooling is available, open the local file and inspect desktop and mobile screenshots for overflow, clipped text, unreadable contrast, and excessive visual density.
