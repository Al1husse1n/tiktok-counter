from telegram import Update 
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from typing import Final
import requests, httpx, os, io
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
FASTAPI_URL = os.getenv("FASTAPI_URL")



#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "This bot helps you count TikTok videos exchanged between two people in a conversation.\n\n"
        "How it works:\n"
        "1️⃣ You export your TikTok message data\n"
        "2️⃣ You upload the file here\n"
        "3️⃣ I analyze it and show you the stats 📊\n\n"
        "Type /help to see step-by-step instructions."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 How to use this bot\n\n"
        "1️⃣ Go to TikTok → Settings → Account → Download your data\n"
        "2️⃣ Request your message data (JSON format)\n"
        "3️⃣ Download the file when it’s ready\n"
        "4️⃣ Upload the file here 📎\n\n"
        "I will:\n"
        "✅ Count TikTok video links\n"
        "✅ Show how many each user sent\n"
        "✅ Give you a clear summary\n\n"
        "⚠️ Your data is processed only for analysis and not shared.\n\n"
        "Send the file whenever you’re ready!"
    )


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if not document.file_name.endswith(".json"):
        await update.message.reply_text("❌ Please send a JSON file only.")
        return

    telegram_file = await document.get_file()
    file_bytes = await telegram_file.download_as_bytearray()
    file_like = io.BytesIO(file_bytes)

    # Save file in user state
    context.user_data["file_like"] = file_like

    await update.message.reply_text(
        "✅ File received.\n\n"
        "Now send the username you want me to analyze."
    )



async def handle_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "file_like" not in context.user_data:
        await update.message.reply_text(
            "⚠️ Please send a JSON file first."
        )
        return

    username = update.message.text.strip()
    file_like = context.user_data.pop("file_like")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FASTAPI_URL}/{username}",
            files={"file": ("chat.json", file_like)},
        )

    if response.status_code != 200:
        await update.message.reply_text(
            response.json().get("detail", "❌ Error processing file.")
        )
        return

    data = response.json()
    average = data.get("your_average", 0)
    await update.message.reply_text(
        f"📊 Results\n\n"
        f"You: {data.get('You', 0)} ({average}%)\n"
        f"{username}: {data.get(username, 0)} ({100 - average}%)"
    )

async def error(update:Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update: {update} caused error: {context.error}")

if __name__ == "__main__":
    print("starting bot...")
    app = Application.builder().token(BOT_TOKEN).build()
    #commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    #messages
    app.add_handler(MessageHandler(filters.TEXT, handle_username))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    app.add_error_handler(error)
    print('Polling')
    app.run_polling(poll_interval=3)