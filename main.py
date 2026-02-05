from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session

import json

app = FastAPI()

engine = create_engine('sqlite:///users.db', connect_args= {'check_some_thread':False})
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id= Column(Integer, primary_key=True, index=True)
    username=Column(String, nullable=False)
Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserResponse(BaseModel):
    id:int
    username:str

app.post('/save_user/{username}', response_model=UserResponse)
async def save_user(username:str, db:Session=Depends(get_db)):
    if db.query(User).filter(User.username == username):
        return{"result":f"{username} is already registered"}
    else:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh()
        return user

@app.post("/analyze/{username}")
async def count_messages(username:str, file:UploadFile = File(...)):
    if not file.filename.endswith('.json'):
        raise HTTPException(400, "I can only process JSON files")
    try:
        contents = await file.read()
        data = json.loads(contents)
        chat_history = (
            data
            .get("Direct Message", {})  
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
            "your_average": round(average_sent)
        }
    except Exception as e:
        raise HTTPException(400, str(e))
