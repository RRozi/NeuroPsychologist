from flet import *
import flet as ft
from GPT import request_
from params import session
from tts import TextToSpeech
from os import path, remove
from playsound import playsound
from stt import stt
from Interface.admin_panel import admin

def PageSession(page: Page):
    def PageEventResize(e: ControlEvent):
        if e.data == "resized" or "enterFullScreen" or "leaveFullScreen":
            _mainContainer.width = page.window_width
            _mainContainer.height = page.window_height
            page.update()
    page.on_window_event = PageEventResize

    def disableOfWisgets(disable: bool) -> None:
        widgets = [Butt_SpeechLastMessage, Butt_MuteSpeech, TextFieldforWrite, SendMessage, SendMessageVOICE, ButtonClearHistory]
        for widget in widgets:
            widget.disabled = disable
        if not disable:
            Butt_SpeechLastMessage.disabled = not session.VOICE_ACTIVE
        page.update()

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
            disableOfWisgets(True)
            ChangeTextField()
            ProgressBar.opacity = 1
            ProgressText.opacity = 1
            page.update()

            # Добавляем сообщение от пользователя в блок чата
            TextField.controls.append(
                ft.Text(
                    text_align=TextAlign.RIGHT,
                    size=16,
                    spans=[
                        ft.TextSpan(
                            '\n' + buffer + '\n',
                            ft.TextStyle(
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=12,
                                    color="#451865",
                                    offset=ft.Offset(1, 8),
                                    blur_style=ft.ShadowBlurStyle.SOLID)
                            )
                        )
                    ]
                )
            )
            ProgressText.value = 'Обработка запроса...'
            page.update()

            # Добавляем сообщение от БОТА в блок чата
            RequestText = request_(buffer)
            TextField.controls.append(
                ft.Text(
                    text_align=TextAlign.LEFT,
                    size=16,
                    spans=[
                        ft.TextSpan(
                            "Нᴇйᴩоᴨᴄихоᴧоᴦ: " + RequestText,
                            ft.TextStyle(shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=16,
                                color="#240623",
                                offset=ft.Offset(1, 8),
                                blur_style=ft.ShadowBlurStyle.SOLID))
                        )
                    ]
                )
            )

            if session.VOICE_ACTIVE:
                ProgressText.value = 'Озвучка текста...'
                ProgressText.update()
                TextToSpeech(RequestText)
            disableOfWisgets(False)
            ChangeTextField()
            ProgressBar.opacity = 0
            ProgressText.opacity = 0
            page.update()

    def voice_change(e):
        session.VOICE_ACTIVE = not session.VOICE_ACTIVE
        Butt_SpeechLastMessage.disabled = not session.VOICE_ACTIVE
        e.control.selected = not e.control.selected
        page.update()
        playsound("static/sounds/tts.mp3")

    def SendInVOICE(e):
        if not stt.MICROPHONE:
            SendMessageVOICE.icon = icons.CANCEL_OUTLINED
            SendMessageVOICE.update()
            stt.status(True)
            for words in stt.listen():
                TextFieldforWrite.value += f"{words} "
                TextFieldforWrite.update()
                ChangeTextField()
        else:
            SendMessageVOICE.icon = icons.MIC_ROUNDED
            SendMessageVOICE.update()
            stt.status(False)
        ...

    def SpeechLastMessage(e):
        if path.exists("audio.mp3") == True:
            disableOfWisgets(True)
            try:
                playsound("audio.mp3")
            except:
                print("Ошибочка :_")
            disableOfWisgets(False)

    def ChangeTextField(e=None) -> None:
        if TextFieldforWrite.value.strip():
            SendMessage.disabled = False
        else:
            SendMessage.disabled = True
        SendMessage.update()


    # DIALOGS - LEAVE
    def Leave(e) -> None:
        if session.HISTORY[1:] == [] and session.CLEAR_HISTORY == False:
            page.go('/')
        else:
            page.dialog = exitConfirmation
            exitConfirmation.open = True
            page.update()

    def selectLeave(e, options) -> None:
        exitConfirmation.open = False
        page.update()
        if options:
            if path.exists("audio.mp3") == True:
                remove("audio.mp3")
            page.go('/feedback')

    # DIALOGS - CLEAR HISTORY
    def clearHistory(e):
        if session.HISTORY[1:] == []:
            pass
        else:
            page.dialog = clearHistoryConfirmation
            clearHistoryConfirmation.open = True
            page.update()

    def SelectClearHistory(e, otions):
        clearHistoryConfirmation.open = False
        page.update()
        if otions:
            TextField.controls.clear()
            TextField.update()
            session.CLEAR_HISTORY = True
            session.HISTORY = session.HISTORY[:1]

    # DIALOGS - APP
    def adminDialog(e):
        page.dialog = admin.ADMIN_PANEL
        admin.ADMIN_PANEL.open = True
        page.update()

    # PAGE DIALOUGUES
    # Диалог потвержлдения выхода с сессии
    exitConfirmation = ft.AlertDialog(
        title=ft.Text("Вы уверены?"),
        content=ft.Text("После выхода вся история общения будет удалена!"),
        actions=[
            ft.TextButton("Да, выйти.", on_click=lambda e: selectLeave(e, True)),
            ft.TextButton("Отмена.", on_click=lambda e: selectLeave(e, False))
        ]
    )

    # Диалог удаления истории
    clearHistoryConfirmation = ft.AlertDialog(
        title=ft.Text("Вы уверены?"),
        content=ft.Text("После очистки бот забудет всю историюю переписки!"),
        actions=[
            ft.TextButton("Да, очистить.", on_click=lambda e: SelectClearHistory(e, True)),
            ft.TextButton("Отмена.", on_click=lambda e: SelectClearHistory(e, False))
        ]
    )

    # Диалог - инфо приложения
    InfoApplication = ft.AlertDialog(
        title=ft.Text("Информация о приложении"),
        content=ft.Text(session.TEXT_INFO)
    )

    # ПрогрессБар во время запроса к GPT
    ProgressBar = ft.ProgressBar(
        width=550,
        color=colors.LIGHT_GREEN_300,
        bgcolor="#eeeeee",
        opacity=0
    )
    ProgressText = ft.Text(
        'Отправка запроса...',
        opacity=0
    )

    # OTHER WIDGETS IN PAGE
    # Кнопка воспроизведения последнего сообщения
    Butt_SpeechLastMessage = ft.IconButton(
        icon=icons.PLAY_CIRCLE_OUTLINE_SHARP,
        tooltip="Озвучить последнее сообщение",
        on_click=SpeechLastMessage
    )

    Butt_MuteSpeech = ft.IconButton(
        icon=icons.VOLUME_UP_OUTLINED,
        selected_icon=icons.VOLUME_OFF_OUTLINED,
        style=ButtonStyle(elevation=3),
        tooltip="Включить/Выключить озвучку",
        on_click=voice_change
    )

    # Поле для отображения диалога
    TextField = ft.ListView(
        auto_scroll=True,
        width=700,
        expand=1,
        spacing=10,
        padding=10
    )

    # Поле ввода для работы с GPT
    TextFieldforWrite = ft.TextField(
        width=700,
        max_lines=1,
        on_change=ChangeTextField,
        on_submit=REQUEST,
        label="Введите сообщение..."
    )
    TextFieldforWrite.width -= 100

    # Кнопка отправка сообщения
    SendMessage = ft.IconButton(
        icons.SEND_ROUNDED,
        disabled=True,
        on_click=REQUEST
    )

    # Кнопка голосовго вввода
    SendMessageVOICE = ft.IconButton(
        icons.MIC_ROUNDED,
        on_click=SendInVOICE
    )

    # Кнопка выхода с сессии
    ButtonLeave = ft.ElevatedButton(
        "Завершить сесcию",
        style=ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)),
        bgcolor=ft.colors.with_opacity(0.6, '#8c2727'),
        color="#ed5f4a",
        on_click=Leave
    )

    # Кнопка удаления истории
    ButtonClearHistory = ft.ElevatedButton(
        "Очистить историю",
        style=ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)),
        bgcolor=ft.colors.with_opacity(0.6, '#8c2727'),
        color="#ed5f4a",
        on_click=clearHistory
    )

    # ОСНОВНОЙ КОНТЕНЕР СО ВСЕМИ ВИДЖЕТАМИ
    _mainContainer = ft.Container(
        gradient=ft.RadialGradient(
            center=Alignment(0.6, -1.25),
            radius=1.2,
            colors=["#42445f",
                    "#1d1e2a"]),
        width=page.width,
        height=page.window_height,
        margin=-10,
        content=ft.Stack([
            ft.Row([
                ft.IconButton(icons.SETTINGS_OUTLINED, icon_size=35, on_click=adminDialog),
            ], spacing=0),
            ft.Column([
                    ft.Container(
                        ft.Column([
                            ft.Container(ft.Row([ProgressBar, ProgressText]), width=700, alignment=alignment.center),
                            ft.Container(
                                TextField,
                                border=border.all(0.7, "#000000"), height=510, border_radius=3
                            ),
                            ft.Row([
                                TextFieldforWrite,
                                SendMessage,
                                SendMessageVOICE
                            ], alignment=MainAxisAlignment.CENTER),
                            ft.Container(
                                ft.Row([
                                    ButtonLeave,
                                    ButtonClearHistory,
                                    Butt_SpeechLastMessage,
                                    Butt_MuteSpeech
                                ]),
                                width=700, alignment=alignment.center, margin=margin.only(bottom=13)
                            )  # Block CONTAINER

                        ], horizontal_alignment=CrossAxisAlignment.CENTER),  # Block COLUMN (end)
                        alignment=alignment.center,
                        margin=margin.only(top=-20)),  # Block CONTAINER

            ], alignment=MainAxisAlignment.CENTER),  # Main block COLUMN
        ])
    )

    return _mainContainer
