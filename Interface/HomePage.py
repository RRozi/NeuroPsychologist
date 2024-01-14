
from flet import *
import flet as ft
from time import sleep
import threading
from playsound import playsound
from params import session


def Home(page: Page):
    def PageEventResize(e: ControlEvent):
        if e.data == "resized" or "enterFullScreen" or "leaveFullScreen":
            _mainContainer.width = page.window_width
            _mainContainer.height = page.window_height
            page.update()
    page.on_window_event = PageEventResize

    def animate() -> None:
        sleep(0.1)
        Title.opacity = 1
        Description.opacity = 1
        page.update()

    def TermsUser(e):
        page.dialog = TermsUserINFO
        TermsUserINFO.open = True
        page.update()

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
        session.DESCRIPTION,
        size=14,
        text_align=TextAlign.CENTER,
        color="#97ab7b",
        opacity=0.0,
        animate_opacity=animation.Animation(duration=510),
        weight=ft.FontWeight.BOLD,

    )

    TermsUserINFO = ft.AlertDialog(
        title=ft.Text("Пользовательское соглашение."),
        content=ft.Text(session.TERMS_TEXT),
    )

    TermsUserText = ft.Row([
        ft.Text("Вы автоматически соглашаетесь с ", size=13),
        ft.Text(
            size=13,
            color="#0186bf",
            selectable=True,
            spans=[
                ft.TextSpan(
                    "условиями использования",
                    style=ft.TextStyle(
                        decoration=ft.TextDecoration.UNDERLINE,
                        decoration_color="#0186bf",
                    ),
                    on_click=TermsUser
                )
            ]
        )
    ],
        alignment=MainAxisAlignment.CENTER,
        spacing=2
    )


    ButtonStartSession = ft.ElevatedButton(
        "Запустить сессию",
        style=ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)),
        width=350,
        height=50,
        bgcolor=ft.colors.with_opacity(0.4, "#356e2d"),
        color="#58ab4d",
        on_click=lambda e: page.go("/session")
    )

    _mainContainer = ft.Container(
        gradient=ft.RadialGradient(
            center=Alignment(0, -1.25),
            radius=1.2,
            colors=["#42445f",
                    "#1d1e2a"]),
        width=page.width,
        height=page.window_height,
        margin=-10,
        content=ft.Stack([
            ft.Column(
                [
                    ft.Container(Title, alignment=alignment.top_center),
                    ft.Container(
                        Description,
                        alignment=alignment.center,
                        margin=margin.only(top=-100)
                    ),
                    ft.Container(
                        ButtonStartSession,
                        alignment=alignment.bottom_center,
                        margin=margin.only(top=110)
                    ),
                    ft.Container(
                        TermsUserText,
                        alignment=alignment.bottom_center,
                    ),
                ],
                alignment=MainAxisAlignment.CENTER
            )
        ])
    )
    threading.Thread(target=animate).start()

    return _mainContainer
