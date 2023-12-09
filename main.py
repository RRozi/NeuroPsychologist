import os
import openai
from dotenv import load_dotenv
load_dotenv()

# OpenAI
openai.api_key = os.getenv("OPENAI")
openai.api_base = "http://localhost:1337/v1"

# data
PSYHOLOGIST_PROMT = """
Ты нейропсихолог[PSYHOLOGIST], твоя задача помогать людям с их состоянием,
как психолог ты не должен обсуждать религиозные, политические темы. Так же запрещенно упоминать темы суицида,
насилия. Ты должен дать понятный и правильный ответ на проблему пациента не зависимо от его возраста.
"""

HISTORY = """
"""

# main
while True:
    HISTORY += "USER:" + input("Ваш запрос: ") + '\n'
    edited_news_text = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": PSYHOLOGIST_PROMT},
                          {"role": "user", "content": HISTORY}],
                stream=False,
            ).choices[0].message.content
    HISTORY += f"PSYHOLOGIST:{edited_news_text}\n"

    print("Нейропсихолог:", edited_news_text)

