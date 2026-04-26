# main.py

import flet as ft
from view.login import LoginPage
from view.menu import MenuPage
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)



class MyApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.on_route_change = self.ruta_principal
        self.page.go("/login")
    
    async def ruta_principal(self, route):
        self.page.views.clear()

        if self.page.route == "/login":
            login_view = LoginPage(self.page)
            self.page.views.append(login_view)
        else:
            menu_page = MenuPage(self.page)
            self.page.views.append(menu_page)
            menu_page.ruta_secundaria()
        self.page.update()

def main(page: ft.Page):
    MyApp(page)

ft.app(target=main, view=ft.WEB_BROWSER, port=8550)

#ft.app(target=main, view=ft.FLET_APP)
