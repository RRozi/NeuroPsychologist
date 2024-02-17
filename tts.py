import threading
import requests
from playsound import playsound
from time import sleep
import re
from params import session
import os


def remove_emojis(text: str):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def text_to_speech(text):
    api = os.getenv("MANDRILL")
    headers = {
        'Authorization': f'Bearer {api}'
    }

    data = {
        "text": text,
        "voice_id": session.VOICE_ID
    }

    response = requests.post("https://api.mandrillai.tech/v1/audio/tts",
                             json=data,
                             headers=headers)
    print(response)

    # Save the file
    if os.path.exists(os.path.join(os.path.dirname(__file__), "audio.mp3")):
        os.remove(os.path.join(os.path.dirname(__file__), "audio.mp3"))
    try:
        with open(os.path.join(os.path.dirname(__file__), "audio.mp3"), "wb") as f:
            f.write(response.content)
            sleep(0.3)
            f.close()
            sleep(0.2)
            threading.Thread(target=playsound, args=(os.path.join(os.path.dirname(__file__), "audio.mp3"),)).start()
    except:
        print("Ошибочка :_")
