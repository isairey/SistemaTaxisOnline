import flet as ft
from view.socios.socio import vista_socios
from view.vehiculos.vehiculo import vista_vehiculos
from view.avances.avance import vista_avances
from view.sanciones.sancion import vista_sanciones
from view.finanzas.finanzas import vista_finanzas
from utils.colors import Colores
from view.menus.menu import vista_menu
from utils.alerts import UtilMensajes
from auth.auth import AuthControlador


class BotonesNevegacion:
    @staticmethod
    def botonesNav(pagina):
        return ft.Column(
            controls=[
                ft.TextButton(
                    "Inicio",
                    scale=1.2,
                    icon=ft.icons.HOME,
                    style=ft.ButtonStyle(
                        icon_color=Colores.BLANCO,
                        color=Colores.BLANCO
                    ),
                    on_click=lambda _: pagina.go("/menu")
                ),
                ft.TextButton(
                    "Socios",
                    scale=1.2,
                    icon=ft.icons.PEOPLE_OUTLINE,
                    style=ft.ButtonStyle(
                        icon_color=Colores.BLANCO,
                        color=Colores.BLANCO
                    ),
                    on_click=lambda _: pagina.go("/socios")
                ),
                ft.TextButton(
                    "Vehiculos",
                    scale=1.2,
                    icon=ft.icons.LOCAL_TAXI_OUTLINED,
                    style=ft.ButtonStyle(
                        icon_color=Colores.BLANCO,
                        color=Colores.BLANCO
                    ),
                    on_click=lambda _: pagina.go("/vehiculos")
                ),
                ft.TextButton(
                    "Avances",
                    scale=1.2,
                    icon=ft.icons.WORK_OUTLINE,
                    style=ft.ButtonStyle(
                        icon_color=Colores.BLANCO,
                        color=Colores.BLANCO
                    ),
                    on_click=lambda _: pagina.go("/avances")
                ),
                ft.TextButton(
                    "Sanciones",
                    scale=1.2,
                    icon=ft.icons.REPORT_OUTLINED,
                    style=ft.ButtonStyle(
                        icon_color=Colores.BLANCO,
                        color=Colores.BLANCO
                    ),
                    on_click=lambda _: pagina.go("/sanciones")
                ),
                ft.TextButton(
                    "Finanzas",
                    scale=1.2,
                    icon=ft.icons.PAYMENTS_OUTLINED,
                    style=ft.ButtonStyle(
                        icon_color=Colores.BLANCO,
                        color=Colores.BLANCO
                    ),
                    on_click=lambda _: pagina.go("/finanzas")
                ),
            ],
            alignment=ft.MainAxisAlignment.END
        )


class MenuPage(ft.View):
    def __init__(self, pagina: ft.Page):
        super().__init__(route="/menu")
        self.pagina = pagina
        self.bgcolor = Colores.NEGRO2
        self.authControlador = AuthControlador(self.pagina)
        #self.rol = self.authControlador.obtener_rol()
        self.nombre_usuario = self.authControlador.obtener_nombre_usuario()
        self.area_contenido = ft.Container(
            content=ft.Column(
                controls=[],
                spacing=10
            ),
            expand=True,
        )

        avatar = ft.Container(
            content=ft.Icon(
            name=ft.icons.PERSON_OUTLINE,
            size=64,
            color=Colores.AMARILLO1
            ),
            width=64,
            height=64,
            alignment=ft.alignment.center
        )

        user_header = ft.Container(
            content=ft.Column(
            controls=[
                avatar,
                ft.Text(
                #self.rol,
                self.nombre_usuario,
                size=20, 
                weight="bold",  
                color=Colores.AMARILLO1,  
                text_align=ft.TextAlign.CENTER
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,  
            spacing=4
            ),
            alignment=ft.alignment.center  
        )

        barra_lateral = ft.Container(
            content=ft.Column(
            controls=[
                user_header,
                ft.Divider(color=Colores.AMARILLO1,),
                BotonesNevegacion.botonesNav(pagina),
                ft.Container(
                content=ft.Column(
                    controls=[
                    ft.Text(
                        "J-31341271-6",
                        color=Colores.DORADO,
                        size=16,
                        weight="bold",
                        font_family="Arial Black Italic",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Versión 1.0.0",
                        color=Colores.DORADO,
                        size=13,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ],
                    spacing=2,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                alignment=ft.alignment.bottom_center,
                padding=ft.padding.only(top=60)
                )
            ],
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[Colores.GRIS, Colores.AZUL2]
            ),
            width=140,
            padding=16,
            border_radius=ft.BorderRadius(0, 0, 0, 0),
            alignment=ft.alignment.top_center
        )

        barra_superior = ft.Container(
            content=ft.Row(
            controls=[
                ft.Text(
                "  Línea San Agatón",
                color=Colores.BLANCO,
                size=30,
                weight="bold",
                expand=True,
                font_family="Arial Black Italic",
                italic=True
                ),
                ft.IconButton(
                icon=ft.icons.DESCRIPTION_OUTLINED,
                icon_color=Colores.BLANCO,
                tooltip="Manual de Usuario",
                on_click=lambda e: pagina.launch_url("https://download856.mediafire.com/aft4fqwp4ozgeojMN_UEwfOtQrHcGbZXhoRIIxqBgDM9ErkwF5g0MDLsv_WW7YmOyc6g81KRAIkrK_extTioNZGn423osE2-HkuEKdpQEQz9VYIzMO3c6VKPzUgW1rSm01A6mlztTGnuyqOUt-xu8YLVw8FhWeoCPDuIh-PxKdzb/sdhh34p5jeh3a4l/Manual_de_usuario_2025+1.2.pdf")
                ),
                ft.IconButton(
                icon=ft.icons.LOGOUT,
                icon_color=Colores.ROJO,
                tooltip="Cerrar sesión",
                on_click=lambda e: UtilMensajes.confirmar_material(
                    page=pagina,
                    titulo="Confirmar Cierre de Sesión",
                    mensaje="¿Está seguro de cerrar sesión?",
                    on_confirm=lambda e: pagina.go("/login"),
                    on_cancel=lambda e: print("Cierre de sesión cancelado")
                )
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.top_right,
            colors=[Colores.GRIS, Colores.AZUL2]
            ),
            height=50,
            border_radius=ft.BorderRadius(0, 0, 0, 0),
            alignment=ft.alignment.center_left
        )

        self.controls = [
            ft.Container(
                gradient=ft.RadialGradient(
                    center=ft.alignment.top_center,
                    radius=1,
                    colors=[Colores.NEGRO1, Colores.NEGRO2, Colores.AZUL2]
                ),
                content=ft.Stack(
                    controls=[
                        ft.Image(
                            src="https://iili.io/3XTug5P.png",
                            fit=ft.ImageFit.CONTAIN,
                            opacity=0.06,
                            expand=True
                        ),
                        ft.Column(
                            controls=[
                                barra_superior,
                                ft.Row(
                                    controls=[barra_lateral, self.area_contenido],
                                    expand=True
                                )
                            ],
                            expand=True,
                            spacing=5
                        )
                    ],
                    expand=True
                ),
                expand=True
            )
        ]

    def ruta_secundaria(self):
        ruta_actual = self.pagina.route

        if ruta_actual == "/socios":
            contenido = vista_socios(self.pagina)
        elif ruta_actual == "/vehiculos":
            contenido = vista_vehiculos(self.pagina)
        elif ruta_actual == "/avances":
            contenido = vista_avances(self.pagina)
        elif ruta_actual == "/sanciones":
            contenido = vista_sanciones(self.pagina)
        elif ruta_actual == "/finanzas":
            contenido = vista_finanzas(self.pagina)
        else:
            contenido = vista_menu(self.pagina)

        self.area_contenido.content = contenido
        self.pagina.update()