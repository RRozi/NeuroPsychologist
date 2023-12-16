
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
from dotenv import load_dotenv
from flet import *
import flet as ft
from flet_navigator import VirtualFletNavigator

load_dotenv()

from Interface.HomePage import Home
from Interface.SessionPage import PageSession


# function loggings
def loggout() -> None:
    """
    logging.debug - write in logs debug info \n
    logging.info - write in logs info \n
    logging.warning - write in logs warning info
    logging.error - write in logs error info
    """
    logging.root.handlers = []
    log_file_name = datetime.datetime.now().strftime("%Y-%m-%d")


    # Создаем обработчик для записи в файл, при этом каждый раз добавляя логи в конец файла
    file_handler = TimedRotatingFileHandler(f'logs/app_{log_file_name}.log', when='midnight', interval=1, backupCount=30,
                                            encoding='utf-8')
    #file_handler.setLevel(logging.DEBUG)

    # Создаем форматирование для сообщений логов (включая дату, имя уровня логирования и текст сообщения)
    formatter = logging.Formatter('%(asctime)s | [%(levelname)s] > %(message)s', datefmt='%y.%m.%d-%H:%M:%S')
    file_handler.setFormatter(formatter)

    # Присвоение обработчика корневому логгеру
    logging.root.addHandler(file_handler)
    logging.root.setLevel(logging.INFO)
loggout()

def main(page: Page) -> None:
    page.title = "Нейропсихолог"
    page.window_width = 650
    page.window_height = 1000
    page.window_resizable = False
    page.window_maximizable = False
    page.theme_mode = ThemeMode.DARK
    page.bgcolor = ft.colors.PURPLE
    page.fonts = {
        "Borsok": "/fonts/Borsok.ttf",
        "Comic": "/fonts/Comic.otf"
    }
    page.update()

    flet_navigator = VirtualFletNavigator(
         {
            '/': Home,
            'session': PageSession
         },
    )
    flet_navigator.render(page)

app(target=main, assets_dir="static")

