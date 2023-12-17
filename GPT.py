import json
from db import connect, cursor
import time
import logging
import os
from openai import OpenAI
from layout import session

# OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI"),
    base_url="http://localhost:1337/v1"
)

# function write info in history
def add_History(role: str, content: str) -> None:
    session.HISTORY.append(
        {
            "role":role,
            "content":content
        }
    )

def request_(UserPromt: str, time_out = 1) -> str:
    try:
        add_History("user", UserPromt)  # Запись ответа ПОЛЬЗОВАТЕЛЯ в ИСТОРИЮ
        request = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=session.HISTORY,
            stream=False,
        ).choices[0].message.content
        add_History("assistant", request)  # Запись ответа GPT в ИСТОРИЮ

        if session.USER_SESSION_ID:
            cursor.execute("UPDATE sessions SET history = ? WHERE id = ?",
                           (json.dumps(session.HISTORY[1:], indent=4, ensure_ascii=False), session.USER_SESSION_ID))
            connect.commit()

        else:
            cursor.execute("INSERT INTO sessions (history) VALUES (?)",
                           (json.dumps(session.HISTORY[1:], indent=4, ensure_ascii=False),))
            connect.commit()
            session.USER_SESSION_ID = session.USER_SESSION_ID = cursor.lastrowid

    except TypeError:
        logging.error(f"Ошибка при попытке ответить на вопрос! \n Сессия ---> {session.HISTORY}")
        time.sleep(time_out)
        request_(UserPromt, time_out + 3)

    else:
        print("Нейропсихолог:", request)
        logging.info(f"Ответ дан корректно.")
        return request