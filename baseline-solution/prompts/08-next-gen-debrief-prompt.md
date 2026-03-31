# 08 Next-Gen Debrief Prompt

Author: Claude Code

## Prompt Purpose

Instruct an agent to write a short, plain-language debrief document for an NHS clinical contact
who has no technical background and no prior connection to the hackathon. The output is a
standalone markdown file that can be sent as-is, or used as the basis for an email or letter.

## Context

This debrief is needed before the next hackathon can be formally invited. An NHS contact —
currently unknown by name, to be reached via an intermediary — needs to understand what the
hackathon is, what happened in the first one, and what is being asked of NHS clinical staff for
the next event.

The first hackathon tackled a real colorectal cancer MDT data problem: extracting structured
patient data from unstructured Word documents used by clinical teams. Student teams built AI
pipelines to automate that extraction. The second hackathon continues that model — student teams
solving real NHS pain points — and NHS clinical input on the day is a core part of what makes
it work.

## Task

You are writing a debrief document for a senior NHS clinical contact with no technical background.

Write the document to `baseline-solution/reports/next-gen-debrief-<your agent name>.md`.

Use the following rules without exception:

- **Maximum 200 words.** Count them. Cut anything that does not earn its place.
- **No buzzwords.** Do not write: AI-powered, transformative, innovative, cutting-edge,
  leveraging, stakeholder, seamless, or any similar filler.
- **No jargon.** If a clinical administrator would not recognise a term in five seconds, cut it
  or replace it with plain English.
- **No hype.** State what happened and what is being asked. Do not oversell.
- **Lead with the ask.** The reader needs to know quickly what they are being invited to do.

## Required Content

The document must cover all of the following, in a natural order that serves the reader:

1. What the hackathon is and what it aims to do.
   - Students work on real healthcare problems over several days.
   - The goal is to find practical tools that could reduce workload or improve care.

2. What happened in the first hackathon.
   - The clinical problem was: extracting structured data from colorectal MDT outcome Word
     documents, which clinical teams currently do by hand.
   - Student teams built software tools to automate that extraction.
   - This is the kind of administrative burden the hackathon is designed to address.

3. The invitation for the next hackathon.
   - Dates: April 13–17, 2026.
   - NHS clinical staff are invited to attend on **Thursday 17 April, 10:00–15:30**.
   - Venue: Richmond American University London, Building 12, Chiswick Park,
     566 Chiswick High Road, London W4 5AN.

4. What NHS staff are asked to do on the day.
   - Share their perspective on what the student teams have built.
   - Provide feedback from a clinical or operational point of view.

5. The call for future problem statements.
   - We want to hear about other pain points relevant to the NHS — whether clinical,
     administrative, IT-related, or operational — that could be posed as real challenges to
     student teams in future events.

## Output Format

Write the document in plain markdown. Use a short title, then prose paragraphs. Do not use
bullet lists in the output — this is a letter-style document, not a slide deck.

Use this exact filename:

```
baseline-solution/reports/next-gen-debrief-<your agent name>.md
```

Replace `<your agent name>` with your actual agent name in lowercase with hyphens
(e.g. `next-gen-debrief-gemini.md`, `next-gen-debrief-claude.md`).

## After Writing The Document

Update `baseline-solution/work-diary.md` with a diary entry recording:
- what you inspected
- what you wrote and why
- which prompt you followed

Sign the entry with your agent name.

## Author Attribution

This prompt was authored by Claude Code.
