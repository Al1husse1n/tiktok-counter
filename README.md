TikTok Chat Analyzer Bot

A Telegram bot powered by FastAPI that analyzes your exported TikTok chat JSON data. It counts messages, video links, and provides a clear summary of interactions between you and another user.

Features

✅ Accepts TikTok chat JSON files via Telegram.

✅ Counts messages sent by you vs the target username.

✅ Calculates the percentage of messages you sent.

✅ Provides a simple, readable summary directly in Telegram.

✅ Fully asynchronous and fast with httpx + python-telegram-bot v20+.

🔒 Your data is processed locally and not shared.

Requirements

Python 3.10+

Libraries:

pip install fastapi uvicorn python-telegram-bot httpx python-dotenv


Telegram bot token (from @BotFather
)

FastAPI server URL (local or deployed)

Project Structure
project/
├── main.py          # FastAPI backend handling JSON analysis
├── bot.py           # Telegram bot client
├── .env             # Environment variables (BOT_TOKEN, FASTAPI_URL)
└── README.md        # Documentation

Setup Instructions
1️⃣ FastAPI Backend

Create a virtual environment:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Install dependencies:

pip install fastapi uvicorn


Run the backend:

uvicorn main:app --reload


Default host: 127.0.0.1

Default port: 8000

Endpoint example: POST http://127.0.0.1:8000/analyze/{username}

Test locally using Swagger UI:

Open: http://127.0.0.1:8000/docs

Upload a JSON file and enter a username.

2️⃣ Telegram Bot Setup

Install bot dependencies:

pip install python-telegram-bot httpx python-dotenv


Create a .env file:

BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
FASTAPI_URL=http://127.0.0.1:8000/analyze


Run the bot:

python bot.py


Interact with your bot:

/start → Welcome message

/help → Step-by-step instructions

Upload a TikTok JSON file

Send the username you want to analyze

How it Works
FastAPI (main.py)

Receives a POST request with a JSON file and username.

Checks if the file is a valid JSON.

Parses Direct Message → Direct Messages → ChatHistory.

Finds the chat with the target username.

Counts:

Messages sent by you

Messages sent by the target username

Calculates the percentage of your messages.

Returns results as JSON:

{
  "You": 14,
  "_.kennaol": 9,
  "your_average": 61
}

Telegram Bot (bot.py)

Receives file via Telegram.

Downloads file bytes and sends it to FastAPI.

Asks user for the username to analyze.

Sends the result back to Telegram:

📊 Results

You: 14 (61%)
_.kennaol: 9 (39%)

Usage Example

Export your TikTok message data (JSON) from TikTok.

Send the JSON file to the bot.

Enter the username you want to analyze.

Receive the analysis summary directly in Telegram.

Notes

Only JSON files are supported. Sending other file types will return an error.

Make sure the username exists in the exported JSON.

The bot processes messages asynchronously and uses httpx for FastAPI requests.

Your data is not stored permanently; it’s only processed for analysis.

Future Improvements

Add support for multiple usernames at once.

Analyze emoji usage, links, and media content.

Deploy FastAPI to a public server and update FASTAPI_URL.

Add conversation state for easier username selection.

Integrate with databases to save past analyses (optional).

License

This project is open-source for educational and personal use.