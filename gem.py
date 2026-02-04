from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
client = genai.Client(api_key=API_KEY)

def ai_reply(text:str, user:str):
    prompt = f""" 
you are in a telegram bot that counts the number of tiktoks sent between two users
when provided with a json file from tiktok exports and username of the other user
and your role is only to reply to texts from bot user
- The bot user who is called {user} sent the text {text}
- Keep your response concise(under 100 words)
- if the user asks how the bot works, tell them that they first need to upload the json then the username
- the user haven't sent a JSON file yet
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        print(f"Gemini error: {e}")
        if("429" in str(e)):
            return "🤖 I'm getting too many requests right now. Please wait a bit and try again."
        return "🤖 I'm having trouble replying right now. Try again later."


