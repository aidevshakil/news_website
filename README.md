# AI News Automation Bot 🤖📰

An autonomous, multi-agent AI News Automation Bot built with **Python**, **CrewAI Framework**, **Slack API Integration**, **Google Sheets Data Logging**, and **Vercel Cron Automation**.

---

## 🌟 Features & Tool Overview

1. **News Fetcher Tool (`src/tools/news_fetcher_tool.py`)**:
   - Uses web search APIs (**SerperDev API** or **Google News RSS**) to discover trending articles on selected topics (AI, Tech, Finance, Crypto).
   - Returns article titles, snippets, source links, and dates.

2. **Intelligent Summarizer Tool (`src/tools/summarizer_tool.py`)**:
   - Uses **Groq / OpenAI LLMs** to generate concise, bulleted summaries.
   - Automatically deduplicates news stories and extracts key takeaways.

3. **Slack Bot Integration Tool (`src/tools/slack_bot_tool.py`)**:
   - Posts formatted news updates in real time to Slack channels using **Slack Block Kit** (via Slack Webhooks or Slack SDK).

4. **Google Sheets Logger Tool (`src/tools/sheets_logger_tool.py`)**:
   - Logs structured news records (`Date`, `Headline`, `Summary`, `Source URL`) into Google Sheets via `gspread` (with fallback local CSV recording).

5. **Multi-Agent Orchestration (`src/crew/`)**:
   - Built with **CrewAI**: `Senior News Researcher`, `Intelligent News Summarizer & Editor`, and `Newsroom Distribution Specialist`.

6. **Hands-Free Cron Automation (`api/cron.py` & `vercel.json`)**:
   - Deploys on **Vercel** as a Python Serverless Function scheduled to run automatically every 6 hours (`0 */6 * * *`).

---

## 📁 Project Structure

```
.
├── README.md                   # Complete documentation
├── requirements.txt            # Python dependencies (crewai, gspread, slack-sdk, etc.)
├── .env.example                # Environment variables template
├── main.py                     # CLI entry point to trigger the bot manually
├── vercel.json                 # Vercel deployment & 6-hour Cron configuration
├── api/
│   └── cron.py                 # Vercel Python Serverless Function handler
└── src/
    ├── __init__.py
    ├── crew/                   # Multi-Agent CrewAI package
    │   ├── __init__.py
    │   ├── agents.py           # CrewAI Agent definitions
    │   ├── tasks.py            # CrewAI Task definitions
    │   └── main_crew.py        # CrewAI pipeline orchestrator
    └── tools/                  # Custom Multi-Agent Tools
        ├── __init__.py
        ├── news_fetcher_tool.py# Tool 1: SerperDev / Google News Fetcher
        ├── summarizer_tool.py  # Tool 2: Groq / OpenAI LLM Summarizer
        ├── slack_bot_tool.py   # Tool 3: Slack Bot Block Kit Publisher
        └── sheets_logger_tool.py # Tool 4: Google Sheets & CSV Data Logger
```

---

## 🚀 Quickstart & Local Setup

### 1. Installation
Clone the repository and install the dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your API credentials:
```bash
cp .env.example .env
```

Environment variables:
* `SERPER_API_KEY`: API key from [Serper.dev](https://serper.dev) for Google News search.
* `GROQ_API_KEY` or `OPENAI_API_KEY`: API key for LLM summarization.
* `SLACK_WEBHOOK_URL` or `SLACK_BOT_TOKEN`: Slack integration URL or bot token.
* `GOOGLE_SHEET_ID` & `GOOGLE_SHEETS_CREDENTIALS_JSON`: Google Sheets service account credentials.

### 3. Run Locally
Run the news bot via terminal:
```bash
python3 main.py AI Tech Crypto
```

---

## ⚡ Deployment on Vercel

1. Push your code to GitHub.
2. Import the repository in [Vercel](https://vercel.com).
3. Add your Environment Variables in the Vercel project settings.
4. Deploy! Vercel automatically detects `vercel.json` and runs `/api/cron` every 6 hours hands-free.
