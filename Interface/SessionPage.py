from flet import *
import flet as ft
from GPT import request_
from params import session
from tts import text_to_speech
from os import path, remove
from playsound import playsound
import os
from stt import stt
from Interface.admin_panel import admin


def PageSession(page: Page):
    def page_event_resize(e: ControlEvent):
        if e.data == "resized" or "enterFullScreen" or "leaveFullScreen":
            _mainContainer.width = page.window_width
            _mainContainer.height = page.window_height
            page.update()

    page.on_window_event = page_event_resize

    def disable_of_wisgets(disable: bool) -> None:
        widgets = [butt_speech_last_message, butt_mute_speech, text_field_for_write, send_message, send_message_voice,
                   button_clear_history]
        for widget in widgets:
            widget.disabled = disable
        if not disable:
            butt_speech_last_message.disabled = not session.VOICE_ACTIVE
        page.update()

    # PAGE FUNCTIONS
    def REQUEST(e) -> None:
        """
        Основная функция связи с функцией работы GPT.
        Связь GUI и модуля работы с OpenAI
        REQUEST(e) ---> request_() ---> GPT
        """
        if text_field_for_write.value.strip():
            buffer = text_field_for_write.value
            text_field_for_write.value = ''
            disable_of_wisgets(True)
            send_message_voice.icon = icons.MIC_ROUNDED
            send_message_voice.update()
            stt.status(False)
            ChangeTextField()
            info_progress_bar.opacity = 1
            progress_text.opacity = 1
            page.update()

            # Добавляем сообщение от пользователя в блок чата
            chat_text_field.controls.append(
                    ft.Text(
                        text_align=TextAlign.RIGHT,
                        size=16,
                        selectable=True,
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
            progress_text.value = 'Обработка запроса...'
            page.update()

            # Добавляем сообщение от БОТА в блок чата
            request_text = request_(buffer)
            chat_text_field.controls.append(
                ft.Row([
                    ft.Text(
                        text_align=TextAlign.LEFT,
                        width=400,
                        selectable=True,
                        size=16,
                        spans=[
                            ft.TextSpan(
                                "Киберпсихолог: " + request_text,
                                ft.TextStyle(
                                    color=ft.colors.LIGHT_GREEN_300,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=16,
                                        color="#240623",
                                        offset=ft.Offset(1, 8),
                                        blur_style=ft.ShadowBlurStyle.SOLID))
                            )
                        ]
                    )
                ])
            )

            if session.VOICE_ACTIVE:
                progress_text.value = 'Озвучка текста...'
                progress_text.update()
                text_to_speech(request_text)
            disable_of_wisgets(False)
            ChangeTextField()
            info_progress_bar.opacity = 0
            progress_text.opacity = 0
            page.update()

    def voice_change(e):
        session.VOICE_ACTIVE = not session.VOICE_ACTIVE
        butt_speech_last_message.disabled = not session.VOICE_ACTIVE
        e.control.selected = not e.control.selected
        page.update()
        playsound("static/sounds/tts.mp3")

    def SendInVOICE(e):
        if not stt.MICROPHONE:
            send_message_voice.icon = icons.CANCEL_OUTLINED
            send_message_voice.update()
            stt.status(True)
            for words in stt.listen():
                text_field_for_write.value += f"{words} "
                text_field_for_write.update()
                ChangeTextField()
        else:
            send_message_voice.icon = icons.MIC_ROUNDED
            send_message_voice.update()
            stt.status(False)

    def SpeechLastMessage(e):
        if path.exists(session.AUDIO_PATH):
            disable_of_wisgets(True)
            try:
                playsound(session.AUDIO_PATH)
            except:
                print("Ошибочка :_")
            disable_of_wisgets(False)

    def ChangeTextField(e=None) -> None:
        if text_field_for_write.value.strip():
            send_message.disabled = False
        else:
            send_message.disabled = True
        send_message.update()

    # DIALOGS - LEAVE
    def Leave(e) -> None:
        if session.HISTORY[1:] == [] and session.CLEAR_HISTORY:
            page.go('/')
        else:
            page.dialog = exit_confirmation
            exit_confirmation.open = True
            page.update()

    def selectLeave(e, options) -> None:
        exit_confirmation.open = False
        page.update()
        if options:
            if path.exists(session.AUDIO_PATH):
                remove(session.AUDIO_PATH)
            page.go('/feedback')

    # DIALOGS - CLEAR HISTORY
    def clear_history(e):
        if not session.HISTORY[1:]:
            pass
        else:
            page.dialog = clear_history_confirmation
            clear_history_confirmation.open = True
            page.update()

    def select_clear_history(e, otions):
        clear_history_confirmation.open = False
        page.update()
        if otions:
            chat_text_field.controls.clear()
            chat_text_field.update()
            session.CLEAR_HISTORY = True
            session.HISTORY = session.HISTORY[:1]

    # DIALOGS - APP
    def admin_dialog(e):
        page.dialog = admin.ADMIN_PANEL
        admin.ADMIN_PANEL.open = True
        page.update()

    # PAGE DIALOUGUES
    # Диалог потвержлдения выхода с сессии
    exit_confirmation = ft.AlertDialog(
        title=ft.Text("Вы уверены?"),
        content=ft.Text("После выхода вся история общения будет удалена!"),
        actions=[
            ft.TextButton("Да, выйти.", on_click=lambda e: selectLeave(e, True)),
            ft.TextButton("Отмена.", on_click=lambda e: selectLeave(e, False))
        ]
    )

    # Диалог удаления истории
    clear_history_confirmation = ft.AlertDialog(
        title=ft.Text("Вы уверены?"),
        content=ft.Text("После очистки бот забудет всю историюю переписки!"),
        actions=[
            ft.TextButton("Да, очистить.", on_click=lambda e: select_clear_history(e, True)),
            ft.TextButton("Отмена.", on_click=lambda e: select_clear_history(e, False))
        ]
    )

    # ПрогрессБар во время запроса к GPT
    info_progress_bar = ft.ProgressBar(
        width=550,
        color=colors.LIGHT_GREEN_300,
        bgcolor="#eeeeee",
        opacity=0
    )
    progress_text = ft.Text(
        'Отправка запроса...',
        opacity=0
    )

    # OTHER WIDGETS IN PAGE
    # Кнопка воспроизведения последнего сообщения
    butt_speech_last_message = ft.IconButton(
        icon=icons.PLAY_CIRCLE_OUTLINE_SHARP,
        tooltip="Озвучить последнее сообщение",
        on_click=SpeechLastMessage
    )

    butt_mute_speech = ft.IconButton(
        icon=icons.VOLUME_UP_OUTLINED,
        selected_icon=icons.VOLUME_OFF_OUTLINED,
        style=ButtonStyle(elevation=3),
        tooltip="Включить/Выключить озвучку",
        on_click=voice_change
    )

    # Поле для отображения диалога
    chat_text_field = ft.ListView(
        auto_scroll=True,
        expand=False,
        width=800,
        spacing=10,
        padding=10
    )

    # Поле ввода для работы с GPT
    text_field_for_write = ft.TextField(
        width=800,
        max_lines=1,
        on_change=ChangeTextField,
        on_submit=REQUEST,
        label="Введите сообщение..."
    )
    text_field_for_write.width -= 100

    # Кнопка отправка сообщения
    send_message = ft.IconButton(
        icons.SEND_ROUNDED,
        disabled=True,
        on_click=REQUEST
    )

    # Кнопка голосовго вввода
    send_message_voice = ft.IconButton(
        icons.MIC_ROUNDED,
        on_click=SendInVOICE
    )

    # Кнопка выхода с сессии
    button_leave = ft.ElevatedButton(
        "Завершить сесcию",
        style=ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)),
        bgcolor=ft.colors.with_opacity(0.6, '#8c2727'),
        color="#ed5f4a",
        on_click=Leave
    )

    # Кнопка удаления истории
    button_clear_history = ft.ElevatedButton(
        "Очистить историю",
        style=ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)),
        bgcolor=ft.colors.with_opacity(0.6, '#8c2727'),
        color="#ed5f4a",
        on_click=clear_history
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
            ft.Column([
                ft.Container(
                    ft.Column([
                        ft.Container(ft.Row([info_progress_bar, progress_text]), width=800, alignment=alignment.center),
                        ft.Container(
                            chat_text_field,
                            border=border.all(0.7, "#000000"), height=550, border_radius=3
                        ),
                        ft.Row([
                            text_field_for_write,
                            send_message,
                            send_message_voice
                        ], alignment=MainAxisAlignment.CENTER),
                        ft.Container(
                            ft.Row([
                                button_leave,
                                button_clear_history,
                                butt_speech_last_message,
                                butt_mute_speech
                            ]),
                            width=800, alignment=alignment.center, margin=margin.only(bottom=13)
                        )  # Block CONTAINER

                    ], horizontal_alignment=CrossAxisAlignment.CENTER),  # Block COLUMN (end)
                    alignment=alignment.center,
                    margin=margin.only(top=-20)),  # Block CONTAINER

            ], alignment=MainAxisAlignment.CENTER),  # Main block COLUMN
            ft.Row([
                ft.Container(ft.IconButton(icons.SETTINGS_OUTLINED, icon_size=35, on_click=admin_dialog)),
            ], spacing=10),
        ])
    )

    return _mainContainer
