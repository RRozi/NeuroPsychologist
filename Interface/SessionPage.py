from flet import *
import flet as ft
from flet_navigator import PageData
from GPT import request_
from layout import session
from db import connect, cursor

def PageSession(pg: PageData):

    # PAGE FUNCTIONS
    def REQUEST(e) -> None:
        """
        Основная функция связи с функцией работы GPT.
        Связь GUI и модуля работы с OpenAI
        REQUEST(e) ---> request_() ---> GPT
        """
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
        session.SessionReset()
        pg.page.update()

        pg.navigator.navigate_homepage(pg.page)

    def Leave(e) -> None:
        if session.HISTORY[1:] == []:
            confirmLeave()
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
        cursor.execute("UPDATE sessions SET history = ? WHERE id = ?", ("История удалена.", session.USER_SESSION_ID))
        connect.commit()
        session.HISTORY = session.HISTORY[:1]
        clearHistoryConfirmation.open = False
        pg.page.update()

    def cancelСlrHistory(e):
        pg.page.dialog = clearHistoryConfirmation
        clearHistoryConfirmation.open = False
        pg.page.update()

    # DIALOGS - BUG REPORT
    def bugReport(e):
        pg.page.dialog = bugReportDialog
        bugReportDialog.open = True
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


    bugReportDialog = ft.AlertDialog(
        title=ft.Text("Нашли ошибку?"),
        content=ft.Text("Если вы обнаружили ошибки/баги/недоработки \nили сбои во время работы приложения \nОтправте нам сообщение")

    )

    InfoApplication = ft.AlertDialog(
        title=ft.Text("Информация о приложении"),
        content=ft.Text(session.textInfo)
    )

    # OTHER WIDGETS IN PAGE
    TextField = ft.TextField(
        multiline=True,
        width=550, min_lines=19,
        read_only=True,
        text_style=ft.TextStyle(shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=16,
                                color="#240623",
                                offset=ft.Offset(1, 8),
                                blur_style=ft.ShadowBlurStyle.SOLID))
    )
    TextFieldforWrite = ft.TextField(
        multiline=True,
        width=550,
        max_lines=1,
        on_change=ChangeTextField,
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
        height=1000,
        margin=-10,
        content=ft.Stack([
            ft.Row([
                ft.IconButton(icons.INFO_OUTLINE, icon_size=35, on_click=infoApp),
                ft.IconButton(icons.BUG_REPORT_OUTLINED, icon_size=35, on_click=bugReport),
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