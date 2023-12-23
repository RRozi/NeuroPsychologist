from flet import *
import flet as ft
from flet_navigator import PageData
from GPT import request_
from layout import session
from db import connect, cursor

def PageSession(pg: PageData):
    def PageEventResize(e: ControlEvent):
        if e.data == "resized" or "enterFullScreen" or "leaveFullScreen":
            _mainContainer.width = pg.page.window_width
            _mainContainer.height = pg.page.window_height
            pg.page.update()

    pg.page.on_window_event = PageEventResize

    # PAGE FUNCTIONS
    def REQUEST(e) -> None:
        """
        Основная функция связи с функцией работы GPT.
        Связь GUI и модуля работы с OpenAI
        REQUEST(e) ---> request_() ---> GPT
        """
        if TextFieldforWrite.value.strip():
            buffer = TextFieldforWrite.value
            TextFieldforWrite.value = ''
            TextFieldforWrite.disabled = True
            TextFieldforWrite.update()
            ChangeTextField()

            TextField.value += f"{buffer}\n\n"
            pg.page.update()

            TextField.value += f"Нᴇйᴩоᴨᴄихоᴧоᴦ: {request_(buffer)}\n\n"
            TextFieldforWrite.disabled = False
            pg.page.update()

    # DIALOGS - LEAVE
    def ChangeTextField(e=None) -> None:
        """
        Проверка поля ввода на пустоту
        """
        if TextFieldforWrite.value.strip():
            SendMessage.disabled = False
            SendMessage.update()
        else:
            SendMessage.disabled = True

            SendMessage.update()

    def cancelLeave(e) -> None:
        exitConfirmation.open = False
        pg.page.update()

    def confirmLeave(e=None) -> None:
        exitConfirmation.open = False
        pg.page.update()
        pg.navigator.navigate("feedback", pg.page)

    def Leave(e) -> None:
        if session.HISTORY[1:] == [] and session.CLEAR_HISTORY == False:
            pg.navigator.navigate_homepage(pg.page)
        else:
            pg.page.dialog = exitConfirmation
            exitConfirmation.open = True
            pg.page.update()

    # DIALOGS - CLEAR HISTORY
    def clearHistory(e):
        if session.HISTORY[1:] == []:
            pass
        else:
            pg.page.dialog = clearHistoryConfirmation
            clearHistoryConfirmation.open = True
            pg.page.update()

    def confirmСlrHistory(e):
        TextField.value = ''
        TextField.update()
        session.CLEAR_HISTORY = True
        session.HISTORY = session.HISTORY[:1]
        clearHistoryConfirmation.open = False
        pg.page.update()

    def cancelСlrHistory(e):
        pg.page.dialog = clearHistoryConfirmation
        clearHistoryConfirmation.open = False
        pg.page.update()

    # DIALOGS - INFO APP
    def infoApp(e):
        pg.page.dialog = InfoApplication
        InfoApplication.open = True
        pg.page.update()

    # PAGE DIALOUGUES
    exitConfirmation = ft.AlertDialog(
        title=ft.Text("Вы уверены?"),
        content=ft.Text("После выхода вся история общения будет удалена!"),
        on_dismiss=cancelLeave,
        actions=[
            ft.TextButton("Да, выйти.", on_click=confirmLeave),
            ft.TextButton("Отмена.", on_click=cancelLeave)
        ]
    )

    clearHistoryConfirmation = ft.AlertDialog(
        title=ft.Text("Вы уверены?"),
        content=ft.Text("После очистки бот забудет всю историюю переписки!"),
        on_dismiss=cancelLeave,
        actions=[
            ft.TextButton("Да, очистить.", on_click=confirmСlrHistory),
            ft.TextButton("Отмена.", on_click=cancelСlrHistory)
        ]
    )

    InfoApplication = ft.AlertDialog(
        title=ft.Text("Информация о приложении"),
        content=ft.Text(session.TEXT_INFO)
    )

    # OTHER WIDGETS IN PAGE
    TextField = ft.TextField(
        multiline=True,
        width=700, min_lines=19, max_lines=19,
        read_only=True,
        text_style=ft.TextStyle(shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=16,
                                color="#240623",
                                offset=ft.Offset(1, 8),
                                blur_style=ft.ShadowBlurStyle.SOLID))
    )
    TextFieldforWrite = ft.TextField(
        width=700,
        max_lines=1,
        on_change=ChangeTextField,
        on_submit=REQUEST,
        label="Введите сообщение..."
    )
    TextFieldforWrite.width -= 50

    SendMessage = ft.IconButton(
        icons.SEND_ROUNDED,
        disabled=True,
        on_click=REQUEST

    )

    ButtonLeave = ft.ElevatedButton(
        "Завершить сесcию",
        style=ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)),
        bgcolor=ft.colors.with_opacity(0.6, '#8c2727'),
        color="#ed5f4a",
        on_click=Leave
    )

    ButtonClearHistory = ft.ElevatedButton(
        "Очистить историю",
        style=ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)),
        bgcolor=ft.colors.with_opacity(0.6, '#8c2727'),
        color="#ed5f4a",
        on_click=clearHistory
    )

    _mainContainer = ft.Container(
        gradient=ft.RadialGradient(
            center=Alignment(0.6, -1.25),
            radius=1.2,
            colors=["#42445f",
                    "#1d1e2a"]),
        width=pg.page.width,
        height=pg.page.window_height,
        margin=-10,
        content=ft.Stack([
            ft.Row([
                ft.IconButton(icons.INFO_OUTLINE, icon_size=35, on_click=infoApp),
            ], spacing=0),
            ft.Column(
                [
                    ft.Container(ft.Column([TextField, ft.Row([TextFieldforWrite, SendMessage], alignment=MainAxisAlignment.CENTER)], horizontal_alignment=CrossAxisAlignment.CENTER), alignment=alignment.center),
                    ft.Container(ft.Row([ButtonLeave, ButtonClearHistory], alignment=MainAxisAlignment.CENTER), alignment=alignment.center_right)
                ],
                alignment=MainAxisAlignment.CENTER
            )
        ])
    )

    pg.page.add(
        _mainContainer
    )