import flet as ft
import re
from datetime import datetime
from utils.colors import Colores
from utils.alerts import UtilMensajes
import httpx


class VehiculosForm:
    def __init__(self, vehiculos_page, titulo: str, accion: str, vehiculo: dict = None):
        self.vehiculos_page = vehiculos_page
        self.page = vehiculos_page.page    
        self.accion = accion
        self.vehiculo = vehiculo or {}
        self.id_vehiculo_actual = self.vehiculo.get("id_vehiculo")

        # Control
        self.campo_control = ft.TextField(
            label="Control",
            value=self.vehiculo.get("numero_control", ""),
            border_radius=0,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO,
            focused_border_color=Colores.AMARILLO1,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=17),
            width=100,
            max_length=5,
            input_filter=ft.NumbersOnlyInputFilter(),
            hover_color=Colores.GRIS00
        )

        # Cédula del propietario
        self.campo_cedula = ft.TextField(
            label="Documento",
            value=self.vehiculo.get("documento", ""),
            border_radius=0,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO,
            focused_border_color=Colores.AMARILLO1,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=17),
            width=180,
            max_length=11,
            hint_text="V-/E-",
            on_change=self.validar_cedula,
            hover_color=Colores.GRIS00
        )

        # Marca
        self.campo_marca = ft.TextField(
            label="Marca",
            value=self.vehiculo.get("marca", ""),
            border_radius=0,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO,
            focused_border_color=Colores.AMARILLO1,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=17),
            width=250,
            max_length=20,
            on_change=self.validar_texto,
            hover_color=Colores.GRIS00
        )

        # Modelo
        self.campo_modelo = ft.TextField(
            label="Modelo",
            value=self.vehiculo.get("modelo", ""),
            border_radius=0,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO,
            focused_border_color=Colores.AMARILLO1,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=17),
            width=250,
            max_length=20,
            on_change=self.validar_texto,
            hover_color=Colores.GRIS00
        )

        # Año
        self.campo_anio = ft.TextField(
            label="Año",
            value=str(self.vehiculo.get("ano", "")),
            border_radius=0,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO,
            focused_border_color=Colores.AMARILLO1,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=17),
            width=100,
            max_length=4,
            input_filter=ft.NumbersOnlyInputFilter(),
            on_change=self.validar_anio,
            hover_color=Colores.GRIS00
        )

        # Placa
        self.campo_placa = ft.TextField(
            label="Placa",
            value=self.vehiculo.get("placa", ""),
            border_radius=0,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO,
            focused_border_color=Colores.AMARILLO1,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=17),
            width=180,
            max_length=8,
            hint_text="ABC123",
            on_change=self.validar_placa,
            hover_color=Colores.GRIS00
        )

        # Botón Guardar
        boton_guardar = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(ft.icons.SAVE, color=Colores.NEGRO1),
                ft.Text(
                    "Agregar" if accion == "agregar" else "Actualizar",
                    color=Colores.NEGRO1,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                )
            ], spacing=5),
            on_click=lambda _: self.guardar_vehiculo(),
            style=ft.ButtonStyle(
                bgcolor=Colores.AMARILLO1,
                shape=ft.RoundedRectangleBorder(radius=0)
            ),
        )

        # Contenedor del formulario
        self.formulario = ft.Container(
            content=ft.Column([
                ft.Row([self.campo_control, self.campo_cedula, self.campo_marca], spacing=15),
                ft.Row([self.campo_modelo, self.campo_anio, self.campo_placa], spacing=15),
                ft.Row([boton_guardar], alignment=ft.MainAxisAlignment.END)
            ]),
            padding=20,
            border_radius=0,
        )

    def guardar_vehiculo(self):

        print(f"DEBUG - accion: {self.accion}")
        print(f"DEBUG - id_vehiculo_actual: {self.id_vehiculo_actual}")
        print(f"DEBUG - vehiculo completo: {self.vehiculo}")

        try:
            datos_vehiculo = {
                "documento": self.campo_cedula.value,
                "numero_control": str(self.campo_control.value),
                "marca": self.campo_marca.value,
                "modelo": self.campo_modelo.value,
                "ano": str(self.campo_anio.value),
                "placa": self.campo_placa.value.upper()
            }
            with httpx.Client() as client:
                if self.accion == "agregar":
                    response = client.post("http://127.0.0.1:8000/vehiculos/", json=datos_vehiculo)

                else:

                    print(f"DEBUG - id_vehiculo_actual: {self.id_vehiculo_actual}")
                    print(f"DEBUG - tipo de id_vehiculo_actual: {type(self.id_vehiculo_actual)}")
                    print(f"DEBUG - datos_vehiculo: {datos_vehiculo}")

                    response = client.put(f"http://127.0.0.1:8000/vehiculos/{self.id_vehiculo_actual}", json=datos_vehiculo)

                    print(f"DEBUG - Status Code: {response.status_code}")
                    print(f"DEBUG - Response Text: {response.text}")

            if response.status_code == 200 or response.status_code == 201:
                UtilMensajes.mostrar_snack(self.page, "Vehículo guardado con éxito", tipo="success")
                
                if hasattr(self.vehiculos_page, "tabla"):
                    self.vehiculos_page.tabla.obtener_vehiculos_api()

                for campo in [
                    self.campo_control, self.campo_cedula,
                    self.campo_marca, self.campo_modelo,
                    self.campo_anio, self.campo_placa
                ]:
                    campo.value = ""
                    campo.error_text = None
                    campo.update()

            elif response.status_code == 422:
                UtilMensajes.mostrar_error(self.page, "Debe agregar un número de control válido para actualizar")
            else:
                try:
        # Intentamos obtener detalle amigable del backend
                    detalle = response.json().get("detail", response.text)
                except Exception:
                    detalle = response.text
                UtilMensajes.mostrar_snack(self.page, f"Error al guardar: {detalle}", tipo="error")
        except Exception as err:
            UtilMensajes.mostrar_snack(self.page, f"Error al guardar: {err}", tipo="error")

    # Validaciones
    def validar_cedula(self, e):
        e.control.error_text = None if ValidacionVehiculo.validar_cedula(e.control.value) else "'V-' o 'E-'"
        e.control.update()

    def validar_texto(self, e):
        e.control.error_text = None if ValidacionVehiculo.validar_texto(e.control.value) else "Solo letras"
        e.control.update()

    def validar_anio(self, e):
        e.control.error_text = None if ValidacionVehiculo.validar_anio(e.control.value) else "1900–" + str(datetime.now().year)
        e.control.update()

    def validar_placa(self, e):
        e.control.error_text = None if ValidacionVehiculo.validar_placa(e.control.value) else "Formato ABC123"
        e.control.update()


class ValidacionVehiculo:
    @staticmethod
    def validar_cedula(cedula: str) -> bool:
        patron = r'^[VE]-\d{7,9}$'
        return re.match(patron, cedula) is not None

    @staticmethod
    def validar_texto(texto: str) -> bool:
        patron = r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]+$'
        return re.match(patron, texto) is not None

    @staticmethod
    def validar_anio(anio: str) -> bool:
        if not anio.isdigit():
            return False
        y = int(anio)
        current = datetime.now().year
        return 1900 <= y <= current

    @staticmethod
    def validar_placa(placa: str) -> bool:
        patron = r'^[A-Z]{3}\d{3,4}$'
        return re.match(patron, placa.upper()) is not None