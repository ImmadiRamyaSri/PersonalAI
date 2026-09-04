# 🧠 Personal AI Executive Assistant

An autonomous AI agent built with **LangChain** and **FastAPI** that acts as an elite executive assistant. It integrates directly with Google Workspace (Gmail & Calendar) and uses audio transcription to generate a consolidated daily briefing and master list of action items.

## 🚀 Key Features
*   **Gmail Integration:** Fetches and filters unread emails from the last 24 hours.
*   **Calendar Integration:** Retrieves today's schedule to identify open time blocks and meeting conflicts.
*   **Audio Transcription:** Uses Groq's `whisper-large-v3` to transcribe meeting recordings and voice notes.
*   **AI Reasoning:** Powered by `qwen/qwen3.8-27b` via LangChain to synthesize disparate data sources into a single, cohesive Morning Briefing.

## 🛠️ Technical Architecture (Single-Tenant)
This v1.0 architecture is designed as a **Single-Tenant** personal productivity tool. 
*   **Authentication:** Uses Google `InstalledAppFlow` to generate local OAuth `token.json` files for secure, browserless API access.
*   **Modularity:** Separated into micro-services (`gmail_service.py`, `calendar_service.py`, `meeting_service.py`) coordinated by a central LangChain brain (`main_assistant.py`).

## 🔮 Future Enhancements: Multi-Tenant SaaS Evolution
To scale this application to allow multiple users to read their own emails and schedules, the architecture will be migrated from local token storage to a complex SaaS model:

1. **Frontend UI:** Build a React/Next.js interface with a "Log in with Google" OAuth button.
2. **OAuth Callback Integration:** Configure Google Cloud Console to send unique user access tokens to the FastAPI backend upon successful login.
3. **Database Layer:** Implement a PostgreSQL database to securely store user-specific OAuth tokens mapped to their unique User IDs.
4. **Dynamic API Requests:** Update the `/generate_briefing` endpoint to accept a session token, look up the specific user's OAuth credentials in the database, and inject them dynamically into the `get_gmail_service()` and `get_calendar_service()` functions, completely replacing the local `.json` file dependency.