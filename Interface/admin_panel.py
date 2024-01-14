from flet import *
import flet as ft
from params import session
from vosk import Model

class Admin:
    def __init__(self):
        self.BODY = ft.Container(
            ft.Column([
                    ft.RadioGroup(
                        on_change=self.change_gpt,
                        value=session.GPT_MODEL,
                        content=ft.Row([
                            ft.Radio(value="gpt-4", label="GPT-4"),
                            ft.Radio(value="gpt-3.5-turbo", label="GPT 3.5t")
                        ])
                    ),
                    ft.Divider(),
                    ft.RadioGroup(
                        on_change=self.change_vosk,
                        value=session.VOSK_MODEL,
                        content=ft.Row([
                            ft.Radio(value="vosk_small", label="VOSK_SMALL_MODEL"),
                            ft.Radio(value="vosk_big", label="VOSK_BIG_MODEL")
                        ])
                    ),
                    ft.Divider(),
                    ft.RadioGroup(
                        on_change=self.change_voice,
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
            title=ft.Text("Временная панель."),
            content=self.BODY
        )

    def change_gpt(self, e):
        session.GPT_MODEL = e.control.value

    def change_voice(self, e):
        session.VOICE_ID = e.control.value

    def change_vosk(self, e):
        session.VOSK_MODEL = e.control.value
        Model(session.VOSK_MODEL)

admin = Admin()