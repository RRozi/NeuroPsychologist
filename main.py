from flet import *
import flet as ft
import os

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
    page.title = "Киберпсихолог"
    page.theme_mode = ThemeMode.DARK
    page.window_height = 800
    page.bgcolor = '#222331'
    page.fonts = {
        "Comic": "/fonts/Comic.otf"
    }

    # Подключение страниц
    router = Router(page)
    page.on_route_change = router.change_route
    page.go('/')


if __name__ == '__main__':
    app(target=main, assets_dir=os.path.join(os.path.dirname(__file__), "static"))
