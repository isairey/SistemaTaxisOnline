import flet as ft
#from datos.datos import datos_de_prueba
import httpx
from utils.colors import Colores
import threading
import time
import asyncio

class Vista_Menu:
    def __init__(self, page: ft.Page):
        self.page = page
            # Referencia a la tarjeta de socios para actualizaciones dinámicas
        self.card_socios = None
        self.card_vehiculos = None
        self.card_avances = None
        self.card_sanciones = None
        self.card_finanzas = None
        self.menu_container = self.build()

    def _create_card(self, title: str, value: str, icon_data):
        card = ft.Container(
            width=150, height=250, padding=10, margin=5,
            border_radius=0, bgcolor="#1f1f26",
            shadow=ft.BoxShadow(color="black", spread_radius=1, blur_radius=5, offset=ft.Offset(2, 2)),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Icon(icon_data, color=Colores.BLANCO, size=60),
                    ft.Text(title, size=14, color=Colores.BLANCO, weight="bold"),
                    ft.Text(value, size=20, weight="bold", color="#cbb1f2"),
                ],
            ),
        )

        # Guardamos referencia para actualizar el valor luego
        if title == "SOCIOS":
            self.card_socios = card
        elif title == "VEHÍCULOS":
            self.card_vehiculos = card
        elif title == "AVANCES":
            self.card_avances = card
        elif title == "SANCIONES":
            self.card_sanciones = card
        elif title == "FINANZAS":
            self.card_finanzas = card

        return card


    def design_cards(self):
        # Cabecera
        header = ft.Container(
            height=60, bgcolor=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#2c2c34", "#161618"],
            ),
            alignment=ft.alignment.center,
        )

                # Inicializamos los valores "Cargando..."; luego se actualizarán desde la API
        cards_info = [
            ("SOCIOS", "Cargando...", ft.icons.PEOPLE_OUTLINE),
            ("VEHÍCULOS", "Cargando...", ft.icons.LOCAL_TAXI_OUTLINED),
            ("AVANCES", "Cargando...", ft.icons.WORK_OUTLINE),
            ("SANCIONES", "Cargando...", ft.icons.REPORT_OUTLINED),
            ("FINANZAS", "Cargando...", ft.icons.PAYMENTS_OUTLINED),
        ]



        cards = [self._create_card(title, value, icon) for title, value, icon in cards_info]


        cards_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=cards
        )

        return ft.Column(
            expand=True,
            controls=[
                header,
                ft.Container(expand=True, padding=20, content=cards_row)
            ]
        )

    
    async def animar_card(self, card: ft.Container, valor_final: int, delay=0.08):
        valor_actual = 0
        step = max(1, valor_final // 20) if valor_final > 20 else 1

        while valor_actual < valor_final:
            valor_actual += step
            if valor_actual > valor_final:
                valor_actual = valor_final

        card.content.controls[2].value = str(valor_actual)

        # Aquí es la clave: actualizar la UI **en el hilo principal**
        self.page.update()  # en vez de card.update()
        await asyncio.sleep(delay)
    
    async def actualizar_contadores(self):
        """Actualiza todos los contadores desde la API de forma sincrónica."""

        if not all([self.card_socios, self.card_vehiculos, self.card_avances,
                    self.card_sanciones, self.card_finanzas]):
            print("Los cards aún no están creados. No se puede actualizar.")
            return
        try:
            async with httpx.AsyncClient() as client:
                            r_socios, r_vehiculos, r_avances, r_sanciones, r_finanzas = await asyncio.gather(
                client.get("http://127.0.0.1:8000/socios"),
                client.get("http://127.0.0.1:8000/vehiculos"),
                client.get("http://127.0.0.1:8000/avances"),
                client.get("http://127.0.0.1:8000/sanciones"),
                client.get("http://127.0.0.1:8000/finanzas"),
            )
            # Obtenemos los totales de forma segura
            total_socios = len(r_socios.json()) if r_socios.status_code == 200 else 0
            total_vehiculos = len(r_vehiculos.json()) if r_vehiculos.status_code == 200 else 0
            total_avances = len(r_avances.json()) if r_avances.status_code == 200 else 0
            total_sanciones = len(r_sanciones.json()) if r_sanciones.status_code == 200 else 0
            total_finanzas = len(r_finanzas.json()) if r_finanzas.status_code == 200 else 0
            # Animamos cada card secuencialmente

                    # Animamos cada card asincrónicamente
            await asyncio.gather(
                self.animar_card(self.card_socios, total_socios),
                self.animar_card(self.card_vehiculos, total_vehiculos),
                self.animar_card(self.card_avances, total_avances),
                self.animar_card(self.card_sanciones, total_sanciones),
                self.animar_card(self.card_finanzas, total_finanzas),

            )


        except Exception as e:
                        # En caso de error, se muestra “Error” en cada card
            for card in [self.card_socios, self.card_vehiculos, self.card_avances,
                     self.card_sanciones, self.card_finanzas]:
                if card:
                    card.content.controls[2].value = "Error"
                    card.update()
            print("Error al actualizar contadores:", e)



    def build(self):
        # Tres secciones principales
        return ft.Container(
            expand=True, padding=5, bgcolor=ft.colors.TRANSPARENT,
            content=ft.Column(
                expand=True, spacing=5, scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(expand=True, padding=20, alignment=ft.alignment.center,
                                 content=ft.Text("¡BIENVENIDO!", weight="bold", size=24, color="white")),
                    ft.Container(expand=True, padding=20, alignment=ft.alignment.center,
                                 content=ft.Text("SISTEMA DE GESTIÓN LINEA SAN AGATÓN", color=Colores.AMARILLO1, size=50, weight="bold", )),
                    ft.Divider(color=Colores.AMARILLO1,),
                    self.design_cards(),
                    
                    
                ]
            )
        )

def vista_menu(page: ft.Page):
    menu = Vista_Menu(page)
    page.add(menu.menu_container)  # mostramos la interfaz de inmediato

    def actualizar_en_hilo():
        import asyncio
        asyncio.run(menu.actualizar_contadores())

    # Ejecutamos la actualización en un hilo separado
    threading.Thread(target=actualizar_en_hilo, daemon=True).start()

    return menu.menu_container