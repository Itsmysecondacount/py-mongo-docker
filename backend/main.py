from fastapi import FastAPI, HTTPException
from model import Timbre
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from telegram import Bot
import requests

# App object
app = FastAPI()

bot = Bot(token="6235736264:AAEqZspl0bgsMpZt5ygWdwJIrs7GDh_LEj4")

from database import (
    fetch_all_todos,
    create_todo,
)

origins = [
    "https://localhost:5173",
    "*",
]  # Para haceptar peticiones del frontEnd en la BD

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"ping": "pong"}


@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response


@app.post("/api/todo", response_model=Timbre)  # Sucede esto
async def post_todo(todo: Timbre):  # Se ejecuta esto
    todo_dict = todo.dict()
    todo_dict["hora"] = datetime.now()

    response = await create_todo(todo_dict)

    if response:
        try:
            await bot.send_message(chat_id="-1001616071693", text=todo_dict["mesage"])
            requests.get("http://192.168.0.56/26/on", timeout=1)
        except Exception as e:
            print("Ocurrió un error: ", e)
            return response
    raise HTTPException(400, "Something went wrong / Bad Request")
