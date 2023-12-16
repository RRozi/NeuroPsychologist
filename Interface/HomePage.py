from flet import *
import flet as ft
from flet_navigator import PageData

import threading
import time

DESCRIPTION = """
Привет! Я твой нейропсихолог, оборудованный ИИ
и помогу тебе понять и улучшить своё психическое здоровье.
Давай обсудим твои мысли, чувства и поведение, 
избегая тем политики, самоубийства, религии, жестокого контента. 
Вместе мы можем добиться замечательных результатов 
"""

def Home(pg: PageData) -> None:
    pg.page.bgcolor = '#222331'
    pg.page.update()
    #pg.navigator.navigate("session", pg.page)

    def animate():
        time.sleep(0.2)

        Title.opacity = 1.0
        Title.offset = (0.07, -2.3)
        Description.opacity = 1.0

        pg.page.update()


    Title = ft.Text(
        size=72,
        text_align=TextAlign.CENTER,
        font_family="Comic",
        color="#dbb932",
        animate_opacity=animation.Animation(duration=950),
        animate_offset=animation.Animation(duration=450),
        offset=ft.Offset(0, -1.5),
        opacity=0.0,
        spans=[
            ft.TextSpan(
                "Нейропсихология",
                ft.TextStyle(shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=16,
                                color="#000000",
                                offset=ft.Offset(1, 10),
                                blur_style=ft.ShadowBlurStyle.SOLID)
                )
            )
        ]
    )

    Description = ft.Text(
        DESCRIPTION,
        size=13,
        text_align=TextAlign.CENTER,
        color="#97ab7b",
        opacity=0.0,
        animate_opacity=animation.Animation(duration=510),
        weight=ft.FontWeight.BOLD,

    )

    ButtonStartSession = ft.ElevatedButton(
        "Запустить сессию",
        style=ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)),
        width=350,
        height=50,
        bgcolor=ft.colors.with_opacity(0.4, "#356e2d"),
        color="#58ab4d",
        on_click=lambda e: pg.navigator.navigate("session", pg.page)
    )

    _mainContainer = ft.Container(
        gradient=ft.RadialGradient(
            center=Alignment(0, -1.25),
            radius=1.2,
            colors=["#42445f",
                    "#1d1e2a"]),
        width=pg.page.width,
        height=1000,
        margin=-10,
        content=ft.Stack([
            ft.Column(
                [
                    Title,
                    ft.Container(
                        Description,
                        alignment=alignment.center,
                        margin=margin.only(top=-250)
                    ),
                    ft.Container(
                        ButtonStartSession,
                        alignment=alignment.bottom_center,
                        margin=margin.only(top=110)
                    ),
                ],
                alignment=MainAxisAlignment.CENTER
            )
        ])
    )

    pg.page.add(
        _mainContainer
    )
    threading.Thread(target=animate).start()