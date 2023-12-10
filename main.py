import os
import openai
import json

from dotenv import load_dotenv
load_dotenv()

# OpenAI
openai.api_key = os.getenv("OPENAI")
openai.api_base = "http://localhost:1337/v1"


# data
PSYHOLOGIST_PROMT = """
Ты нейропсихолог, твоя задача помогать людям с их состоянием,
как психолог ты НЕ ДОЛЖЕН обсуждать и ОТВЕЧАТЬ на религиозные, политические темы. Так же ЗАПРЕЩЕННО упоминать темы суицида, насилия.
При запросе ЗАПРЕЩЁННЫХ тем, отвечай - 'Я как нейропсихолог немогу обсуждать....' 
Ты должен дать понятный и правильный ответ на проблему пациента не зависимо от его возраста. Приветствуй и отвечай как ПСИХОЛОГ

Всё отвечай только на том языке на котором тебе его задали. При запросе ЗАПРЕЩЁННЫ, отвечай - 'Я как нейропсихолог немогу обсуждать....' - без префикса PSYHOLOGIST !
Твоё имя в истории общения PSYHOLOGIST(упоминать его при своём ответе не надо):, а имя пациента USER:
Запрос от пользователя - 
"""

HISTORY = """
"""

# main
while True:
    HISTORY += input("Ваш запрос: ") + '\n'
    edited_news_text = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": PSYHOLOGIST_PROMT
                    },
                    {
                        "role": "user",
                        "content": HISTORY
                    }]
            )['choices'][0]['message']['content']       #.removeprefix("GPT-3.5: ")
    HISTORY += f"PSYHOLOGIST:{edited_news_text}\n"

    print("Нейропсихолог:", edited_news_text)

