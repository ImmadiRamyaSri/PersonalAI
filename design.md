# Personal AI Executive Assistant: Design

## Steps

| # | Step | Type | Input | Output |
|---|------|------|-------|--------|
| 1 | Fetch emails | Tool (Gmail API) | Previous day's emails | Raw emails |
| 2 | Summarize emails | LLM | All of the previous day's emails | Email summary |
| 3 | Fetch calendar | Tool (Calendar API) | Today's calendar | Today's events |
| 4 | Build schedule | LLM | Today's events | Today's schedule |
| 5 | Transcribe meeting | Tool (Whisper) | Meeting recording | Transcript |
| 6 | Summarize meeting | LLM | Transcript | Meeting summary |
| 7 | Write briefing | LLM | All of the above | Morning briefing with priorities |

## Autonomy

Today the assistant is a fixed workflow.
- All steps and tool calls are predefined in my code.
- The LLM only does the tasks assigned to it (summarizing and writing).

Planned agent version (LangGraph):
- The input becomes a request in plain language, such as "Prepare me for my 3 PM meeting".
- The model chooses which tools to call and in what order, and decides when it has enough information.
- Examples of decisions it would make: search emails from a person who appears in a meeting, check the calendar when an email mentions a deadline, skip transcription when there is no audio file.
- A checker step compares the briefing with the source data and fixes anything missing.
- The agent asks before any action with side effects, such as drafting a reply.

## Evals

Component-level checks test one step. End-to-end checks test the final briefing.

### End-to-end

| # | Question | How I check it |
|---|----------|----------------|
| 1 | Does the briefing include every meeting on today's calendar? | Code: compare event titles from the Calendar API with the briefing text |
| 2 | Are spam and promotional emails left out of the email summary? | Code: check the Gmail category label on each email used |
| 3 | Is the briefing clear and correctly prioritized? | LLM as a judge: score from 1 to 5 |

### Component-level

| # | Question | How I check it |
|---|----------|----------------|
| 4 | Does the transcript capture names correctly? | Code: record a short sample with known names, then count how many appear in the transcript |
| 5 | Does each email summary keep the sender and any deadline? | LLM as a judge on a small set of sample emails |

### Test data

I keep a small fixed set of sample emails, calendar events and one audio file, so I can re-run the same checks after every change and compare results between the workflow and the agent.

## Honest scope

### What it does today
- Reads the previous day's emails from Gmail and today's events from Google Calendar.
- Transcribes a local meeting audio file with Whisper (through Groq).
- Uses an LLM to summarize the emails and the meeting, then combines everything into one morning briefing with priorities.
- Runs when I start it. It does not run on its own.

### What it does not do yet
- It is a fixed workflow, not an agent. The order of steps and the tools are decided in my code.
- It does not send emails, reply, or create calendar events.
- It works on a recorded audio file only. It does not join live meetings.
- It has no formal evaluation results yet.

### Planned
Convert it to a LangGraph agent, run the same evals on both versions, and update this file with the results.s