import threading
import requests
from playsound import playsound
from time import sleep
from params import session
import os


def TextToSpeech(text):
    # if os.path.exists("text.mp3") == True:
    #     os.remove("text.mp3")
    #
    # audio = gTTS(text=text, lang='ru', slow=False)
    # audio.save("text.mp3")
    # playsound("text.mp3")
    headers = {
        'Authorization': 'Bearer md-uTMcROuPbsFXnSVkpTmbaYGxatGhjVPJixKlGIuCoPJjYZbE'
    }

    data = {
        "text": text,
        "voice_id": session.VOICE_ID
    }

    response = requests.post("https://api.mandrillai.tech/v1/audio/tts",
                             json=data,
                             headers=headers)

    # Save the file
    if os.path.exists(os.path.join(os.path.dirname(__file__), "audio.mp3")) == True:
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
