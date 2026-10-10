# DevLift AI ⚡

A small AI-powered developer productivity and learning assistant built for the challenge: help people learn faster, work smarter, and understand technology.

## Features
- **Explain code** in plain language
- **Debug a problem** with a structured troubleshooting plan
- **Learn a concept** with a practical 10-minute learning loop
- **Improve my code** using a maintainability and testing checklist
- Adjustable explanation level and preferred programming stack
- Download answers as Markdown
- Works immediately in offline demo mode; optional live AI via an OpenAI-compatible API

## Run locally
Requires Python 3.10+.

```bash
# 1. Extract the zip and open a terminal in this folder
python -m venv .venv

# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the app
streamlit run app.py
```

## Enable live AI
1. Copy `.env.example` to `.env`.
2. Put your API key in `OPENAI_API_KEY`.
3. Optionally set `OPENAI_MODEL` and `OPENAI_BASE_URL`.
4. Restart Streamlit and select **Auto (API if configured)**.

Without a key, the app automatically provides offline demo guidance. The demo does not execute code or pretend to verify a fix.

## Suggested demo (2 minutes)
1. Select **Explain code** and paste:
   ```python
   def is_even(number):
       return number % 2 == 0
   ```
2. Explain how `%` and the returned Boolean work.
3. Switch to **Debug a problem** and describe an off-by-one or type error.
4. Switch to **Learn a concept** and enter `recursion`.
5. Download the answer as Markdown.

## Project structure
- `app.py` — Streamlit application and response logic
- `requirements.txt` — Python dependencies
- `.env.example` — optional API configuration template

## Responsible use
Treat generated suggestions as a starting point. Review and test code before using it in production. Avoid pasting secrets, credentials, or private source code into external AI services.
