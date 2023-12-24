from flet import *
import flet as ft
from flet_navigator import PageData
import json
from layout import session
from GPT import LogInExls
from db import connect, cursor

FeedBackDB = [{
    "score":'',
    "comment":''
}]

def PageFeedBack(pg: PageData):

    def PageEventResize(e: ControlEvent):
        if e.data == "resized" or "enterFullScreen" or "leaveFullScreen":
            _mainContainer.width = pg.page.window_width
            _mainContainer.height = pg.page.window_height
            pg.page.update()

    pg.page.on_window_event = PageEventResize

    Title = ft.Text(
        size=65,
        text_align=TextAlign.CENTER,
        font_family="Comic",
        color="#dbb932",
        spans=[
            ft.TextSpan(
                "Оцените работу",
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

    feedBackMessage = ft.TextField(
        multiline=True,
        min_lines=12, max_lines=12,
        width=700,
        disabled=True
    )

    def selectedScore(e, score: str) -> None:
        FeedBackDB[0]['score'] = score.strip(", ")
        feedBackMessage.value = score
        feedBackMessage.disabled = False
        buttonConfirm.disabled = False
        pg.page.update()
        feedBackMessage.focus()

    def Completion(e):
        FeedBackDB[0]['comment'] = feedBackMessage.value
        cursor.execute("UPDATE sessions SET feedback = ? WHERE id = ?",
                       (json.dumps(FeedBackDB, indent=4, ensure_ascii=False), session.USER_SESSION_ID))
        connect.commit()
        LogInExls(idCol=3, value=FeedBackDB)
        session.SessionReset()
        pg.navigator.navigate_homepage(pg.page)

    scoreIcon = ft.Row([
        ft.IconButton(icons.SENTIMENT_DISSATISFIED_SHARP,
                      icon_color="#B03319",
                      icon_size=46,
                      on_click=lambda e: selectedScore(e, "Ужасно, ")),

        ft.IconButton(icons.SENTIMENT_DISSATISFIED,
                      icon_color="#F15B3C",
                      icon_size=46,

                      on_click=lambda e: selectedScore(e, "Плохо, ")),

        ft.IconButton(icons.SENTIMENT_NEUTRAL,
                      icon_color="#EC9A2C",
                      icon_size=46,
                      on_click=lambda e: selectedScore(e, "Нормально, ")),

        ft.IconButton(icons.SENTIMENT_SATISFIED,
                      icon_color="#49BD17",
                      icon_size=46,
                      on_click=lambda e: selectedScore(e, "Хорошо, ")),

        ft.IconButton(icons.SENTIMENT_SATISFIED_SHARP,
                      icon_color="#58ab4d",
                      icon_size=46,
                      on_click=lambda e: selectedScore(e, "Отлично, "))
    ], alignment=MainAxisAlignment.CENTER)

    buttonConfirm = ft.ElevatedButton(
        "Завершить",
        style=ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)),
        width=350,
        height=50,
        bgcolor=ft.colors.with_opacity(0.4, "#356e2d"),
        color="#58ab4d",
        disabled=True,
        on_click=Completion
    )

    _mainContainer = ft.Container(
        gradient=ft.RadialGradient(
            center=Alignment(0, -1.25),
            radius=1.2,
            colors=["#42445f",
                    "#1d1e2a"]),
        width=pg.page.width,
        height=pg.page.window_height,
        margin=-10,
        content=ft.Stack([
            ft.Column(
                [
                    ft.Container(Title,
                                 alignment=alignment.top_center,
                                 ),
                    ft.Container(
                        scoreIcon,
                        alignment=alignment.center,
                        margin=margin.only(top=30)
                    ),
                    ft.Container(
                        feedBackMessage,
                        alignment=alignment.center
                    ),
                    ft.Container(
                        ft.Column([buttonConfirm]),
                        alignment=alignment.bottom_center,
                    )
                ],
                alignment=MainAxisAlignment.CENTER
            )
        ])
    )

    pg.page.add(
        _mainContainer
    )