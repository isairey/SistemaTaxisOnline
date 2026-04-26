# auth.py
import httpx
import flet as ft
from utils.alerts import UtilMensajes

class AuthControlador:
    def __init__(self, page: ft.Page):
        self.page = page
        self.api_url = "http://localhost:8000"  # URL de la API
        self.token = None
        self.user_info = {}

    async def autenticar(self, username: str, password: str) -> str | None:
        """
        Hace POST /login y si es exitoso guarda token + user_info en session.
        Devuelve el rol (str) o None si falla.
        """
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
                self.token = data.get("access_token", "")
                self.user_info = data.get("usuario", {})

                # Guardar en sesión de Flet para que otras vistas accedan
                self.page.session.set("user_info", self.user_info)
                self.page.session.set("token", self.token)

                #return self.user_info.get("rol", None)
                return True, data
            
            else:
                error_detail = response.json().get("detail", "Error desconocido")
                UtilMensajes.mostrar_snack(self.page, f"Error de autenticación: {error_detail}", tipo="error")
                return False, None

        except httpx.RequestError as e:
            UtilMensajes.mostrar_snack(self.page, f"Error de conexión: {e}", tipo="error")
            return False, None
        except Exception as e:
            UtilMensajes.mostrar_snack(self.page, f"Error inesperado: {e}", tipo="error")
            return False, None

    def obtener_rol(self) -> str | None:
        user_info = self.page.session.get("user_info") or {}
        return user_info.get("rol")

    def obtener_info_usuario(self) -> dict:
        return self.page.session.get("user_info", {})
    
    def obtener_nombre_usuario(self) -> str:
        user_info = self.page.session.get("user_info") or {}
        return user_info.get("nombre_usuario", "Usuario Desconocido")

    async def cerrar_sesion(self):
        self.page.session.remove("user_info")
        self.page.session.remove("token")
        self.user_info = {}
        self.token = None
        await self.page.go_async("/login")

    def obtener_token(self) -> str:
        return self.page.session.get("token", "")

    def esta_autenticado(self) -> bool:
        return bool(self.page.session.get("token", ""))