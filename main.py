from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from typing import List, Optional
from pydantic import BaseModel, Field
import json

app = FastAPI()

@app.post("/analyze/{username}")
async def count_messages(username:str, file:UploadFile = File(...)):
    if not file.filename.endswith('.json'):
        raise HTTPException(400, "I can only process JSON files")
    try:
        contents = await file.read()
        data = json.loads(contents)
        chat_history = (
            data
            .get("Direct Message", {})  #.get(key, default), so it doesnt crash
            .get("Direct Messages", {})
            .get("ChatHistory", {})
        )

        user_found = False
        chat_key = f"Chat History with {username}:"
        for other_username in chat_history.keys(): 
            if other_username == chat_key:
                user_found = True
                user = chat_history.get(other_username)
        if not user_found:
            raise HTTPException(404, "username not found")
        chat_user, other_user = 0,0
        for message in user:
            if username == message.get("From"):
                other_user += 1
            else: 
                chat_user += 1
        average_sent = (chat_user/(chat_user + other_user)) * 100
        return {
            "You": chat_user,
            username: other_user,
            "your_average": average_sent
        }
    except Exception as e:
        raise HTTPException(400, str(e))
