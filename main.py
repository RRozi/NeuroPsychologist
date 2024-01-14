from dotenv import load_dotenv
from flet import *
import flet as ft
from params import session

load_dotenv()

from Interface.HomePage import Home
from Interface.SessionPage import PageSession
from Interface.FeedbackPage import PageFeedBack

class Router:
    def __init__(self, page: ft.Page):
        self.page = page

    def pages(self):
        return {
            "/": Home(self.page),
            "/session": PageSession(self.page),
            "/feedback": PageFeedBack(self.page)
        }

    def change_route(self, e: ft.RouteChangeEvent):
        self.page.views.clear()
        self.page.views.append(
            ft.View(
                controls=[self.pages()[e.route]]
            )
        )
        self.page.update()

def main(page: Page) -> None:
    # Настройка окна
    page.title = "Нейропсихолог " + session.APP_VERSION
    page.theme_mode = ThemeMode.DARK
    page.bgcolor = '#222331'
    page.fonts = {
        "Borsok": "/fonts/Borsok.ttf",
        "Comic": "/fonts/Comic.otf"
    }

    # Подключение страниц
    router = Router(page)
    page.on_route_change = router.change_route
    page.go('/')

if __name__ == '__main__':
    app(target=main, assets_dir="static")
