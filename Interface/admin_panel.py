import flet as ft
from vosk import Model

from params import session


def change_gpt(e):
    session.GPT_MODEL = e.control.value


def change_vosk(e):
    session.VOSK_MODEL = e.control.value
    Model(session.VOSK_MODEL)


def change_voice(e):
    session.VOICE_ID = e.control.value
    if session.VOICE_ID == "21m00Tcm4TlvDq8ikWAM" or "EXAVITQu4vr4xnSDxMaL":
        session.HISTORY.append(
            {
                "role": "system",
                "content": "ТЫ ТЕПЕРЬ ЖЕНСОГО ПОЛА"
            },
        )
    elif session.VOICE_ID == "5Q0t7uMcjvnagumLfvZi" or "GBv7mTt0atIp3Br8iCZE":
        session.HISTORY.append(
            {
                "role": "system",
                "content": "ТЫ ТЕПЕРЬ МУЖСКОГО ПОЛА"
            },
        )

class Admin:
    def __init__(self):
        self.BODY = ft.Container(
            ft.Column([
                    ft.RadioGroup(
                        on_change=change_gpt,
                        value=session.GPT_MODEL,
                        content=ft.Row([
                            ft.Radio(value="gpt-4", label="GPT-4"),
                            ft.Radio(value="gpt-3.5-turbo", label="GPT 3.5t")
                        ])
                    ),
                    ft.Divider(),
                    ft.RadioGroup(
                        on_change=change_vosk,
                        value=session.VOSK_MODEL,
                        content=ft.Row([
                            ft.Radio(value="vosk_small", label="VOSK_SMALL_MODEL"),
                            ft.Radio(value="vosk_big", label="VOSK_BIG_MODEL")
                        ])
                    ),
                    ft.Divider(),
                    ft.RadioGroup(
                        on_change=change_voice,
                        value=session.VOICE_ID,
                        content=ft.Row([
                            ft.Radio(value="21m00Tcm4TlvDq8ikWAM", label="Rachel"),
                            ft.Radio(value="EXAVITQu4vr4xnSDxMaL", label="Sarah"),
                            ft.Radio(value="5Q0t7uMcjvnagumLfvZi", label="Paul"),
                            ft.Radio(value="GBv7mTt0atIp3Br8iCZE", label="Thomas"),
                        ])
                    ),

            ])

        )

        self.ADMIN_PANEL = ft.AlertDialog(
            title=ft.Text("Настройки"),
            content=self.BODY
        )


admin = Admin()