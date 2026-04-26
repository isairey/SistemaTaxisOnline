import flet as ft
import httpx
from auth.auth import AuthControlador
from utils.alerts import UtilMensajes
from utils.colors import Colores
import json
import tracemalloc
tracemalloc.start()


class AuthManager:
    def __init__(self, page):
        self.page = page
        self.api_url = "http://localhost:8000"  # URL de la API
        self.token = None
        self.user_info = None

    async def autenticar(self, username, password):
        try:
            login_data = {
                "nombre_usuario": username,
                "password": password
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/login",
                    json=login_data,
                    headers={"Content-Type": "application/json"},
                    timeout=30.0
                )
            
            if response.status_code == 200:
                data = response.json()
                self.page.session.set("user_info", data.get("usuario", {}))
                self.page.session.set("token", data.get("access_token", ""))
                return True, data
            else:
                error_detail = response.json().get("detail", "Error desconocido")
                return False, error_detail
        except httpx.RequestError as e:
            return False, f"Error de conexión: {str(e)}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
        

class LoginPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/login")
        self.page = page
        self.page.title = "SAN AGATÓN"

        # controlador de autenticación
        self.auth_controlador = AuthControlador(page)

        # mensaje de estado
        self.mensaje = ft.Text("", color=Colores.ROJO)

        # construir UI
        self.vista_login()

    async def login(self, e):
        username = self.username.value.strip()
        password = self.password.value.strip()

        if not username or not password:
            self.mensaje.value = "Usuario y contraseña son requeridos"
            self.mensaje.color = Colores.ROJO
            self.page.update()
            return

        try:
            success, response = await self.auth_controlador.autenticar(username, password)
            if success:
                usuario = response.get("usuario", {})
                nombre_usuario = usuario.get("nombre_usuario", "Desconocido")
                #rol = response.get("usuario", {}).get("rol", "Desconocido")
                UtilMensajes.mostrar_snack(self.page, f"Bienvenido {nombre_usuario}", tipo="success")
                #UtilMensajes.mostrar_snack(self.page, f"Bienvenido {username} (Rol: {rol})", tipo="success")

                rol = response.get("usuario", {}).get("rol", username)
                self.page.session.set("username", nombre_usuario)
                self.page.session.set("rol", rol)
                self.page.session.set("token", response.get("access_token", ""))

                self.page.go("/menu")
            else:
                UtilMensajes.mostrar_snack(self.page, f"Credenciales incorrectas: {response}", tipo="error")
        except Exception as err:
            UtilMensajes.mostrar_snack(self.page, f"Error inesperado: {err}", tipo="error")

        self.page.update()

    # ---------------- UI helpers (similar a lo que ya tenías) ----------------
    def nombre_login(self):
        return ft.Container(
            width=380,  
            height=210,  
            content=ft.Image(
                src="https://iili.io/3RFl75l.png",
                width=380,
                height=210,
                fit=ft.ImageFit.COVER,  
            ),
            alignment=ft.alignment.center,
            padding=0,
        )

    def texto_bienvenida(self):
        return ft.Text(
            "¡Bienvenido de vuelta!",
            weight=ft.FontWeight.BOLD,
            size=20,
            color=Colores.BLANCO,
        )

    def campos_texto(self):
        self.username = ft.TextField(
            label="Usuario",
            label_style=ft.TextStyle(color=Colores.BLANCO, size=20),
            filled=True,
            border_color=ft.colors.TRANSPARENT,    
            hint_text="Ingrese su usuario",
            bgcolor=Colores.NEGRO0,
            width=300,
            height=50,
            border_radius=0,
            prefix_icon=ft.icons.LOGIN,
            focused_border_color=Colores.AMARILLO1,
            hover_color=Colores.GRIS00
        )
        self.password = ft.TextField(
            label="Contraseña", 
            hint_text="Ingrese su contraseña",
            label_style=ft.TextStyle(color=Colores.BLANCO, size=20),
            password=True,
            filled=True,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO0,
            width=300,
            height=50,
            border_radius=0,
            can_reveal_password=True,
            prefix_icon=ft.icons.PASSWORD,
            focused_border_color=Colores.AMARILLO1,
            hover_color=Colores.GRIS00
        )
        return self.username, self.password

    def boton_login(self):
        return ft.ElevatedButton(
            text="INGRESAR",
            on_click=self.login,
            bgcolor=Colores.AMARILLO1,
            color=Colores.GRIS,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                padding=ft.padding.symmetric(horizontal=30, vertical=10)
            )
        )

    def contenedor_login(self):
        logo = self.nombre_login()
        texto_bienvenida = self.texto_bienvenida()
        username, password = self.campos_texto()
        boton_login = self.boton_login()

        return ft.Container(
            content=ft.Column(
            [
                logo,
                ft.Container(height=40),
                texto_bienvenida,
                ft.Container(height=30),
                username,
                password,
                ft.Row(
                [boton_login],
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            ),
            padding=ft.padding.all(10),
            width=425,
            height=650,
            border_radius=0,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(color="black", blur_radius=15, offset=ft.Offset(4, 4)),
            gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[Colores.AZUL3, Colores.AZUL2],
            ),
        )

    def contenedor_fondo(self, contenedor_login: ft.Container):
        background = ft.Container(
            expand=True,
            gradient=ft.RadialGradient(
                center=ft.alignment.top_center,
                radius=1,
                colors=[Colores.NEGRO1,Colores.NEGRO2, Colores.AZUL2]
            ),
            border_radius=0,

        )
       
        stack = ft.Stack(
            controls=[
                background,
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=contenedor_login
                )
            ]
        )

        return ft.Container(content=stack, expand=True)

    def vista_login(self):
        contenedor_login = self.contenedor_login()
        contenedor_fondo = self.contenedor_fondo(contenedor_login)
        self.controls.append(contenedor_fondo)

    """async def login(self, e):
        username = self.username.value
        password = self.password.value

        try:
            rol = await self.auth_controlador.autenticar(username, password)
            if rol:
                
                UtilMensajes.mostrar_snack(self.page, f"Bienvenido {rol}", tipo="success")
                self.page.go("/menu")
            else:
                UtilMensajes.mostrar_snack(self.page, "Credenciales incorrectas", tipo="error")
        except Exception as err:
            UtilMensajes.mostrar_snack(self.page, f"Error: {err}", tipo="error")"""