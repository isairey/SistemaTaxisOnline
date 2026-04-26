import flet as ft
import re
from datetime import datetime
from utils.colors import Colores
from utils.alerts import UtilMensajes
import httpx

class SociosForm:
    def __init__(self, socios_page, titulo, accion, socio=None):
        self.socios_page = socios_page
        self.accion = accion
        self.socio = socio or {}
        self.id_socio_actual = self.socio.get('id_socio')


        self.campo_control = ft.TextField(
            label="Control",
            value=str(self.socio.get("numero_control", "")),
            border_radius=0,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO,
            focused_border_color=Colores.AMARILLO1,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=17),
            width=100,
            max_length=2,
            input_filter=ft.NumbersOnlyInputFilter(),
            hover_color=Colores.GRIS00
        )

        self.campo_cedula = ft.TextField(
            label="Cédula",
            value=self.socio.get("documento", ""),
            border_radius=0,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO,
            focused_border_color=Colores.AMARILLO1,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=17),
            width=125,
            max_length=11,
            hint_text="V-/E-",
            on_change=self.validar_cedula,
            hover_color=Colores.GRIS00
        )
        self.campo_nombres = ft.TextField(
            label="Nombres",
            value=self.socio.get("nombres", ""),
            border_radius=0,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO,
            focused_border_color=Colores.AMARILLO1,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=17),
            width=275,
            max_length=30,
            on_change=self.validar_texto,
            hover_color=Colores.GRIS00
        )
        self.campo_apellidos = ft.TextField(
            label="Apellidos",
            value=self.socio.get("apellidos", ""),
            border_radius=0,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO,
            focused_border_color=Colores.AMARILLO1,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=17),
            width=275,
            max_length=30,
            on_change=self.validar_texto,
            hover_color=Colores.GRIS00
        )

        self.campo_fecha = ft.TextField(
            label="Fecha Nacimiento",
            value=self.socio.get("fecha_nacimiento", ""),
            border_radius=0,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO,
            focused_border_color=Colores.AMARILLO1,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=17),
            width=140,
            max_length=10,
            hint_text="AAAA-MM-DD",
            on_change=self.validar_fecha_nacimiento,
            hover_color=Colores.GRIS00
        )
        self.campo_telefono = ft.TextField(
            label="Teléfono",
            value=self.socio.get("numero_telefono", ""),
            border_radius=0,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO,
            focused_border_color=Colores.AMARILLO1,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=17),
            width=155,
            max_length=15,
            prefix_text="+58 ",
            hint_text="414 1234567",
            input_filter=ft.NumbersOnlyInputFilter(),
            hover_color=Colores.GRIS00
        )
        self.campo_direccion = ft.TextField(
            label="Dirección",
            value=self.socio.get("direccion", ""),
            border_radius=0,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO,
            focused_border_color=Colores.AMARILLO1,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=17),
            width=370,
            max_length=50,
            hint_text="Municipio/Urb/Sector/Calle/Casa",
            multiline=True,
            hover_color=Colores.GRIS00
        )
        self.campo_rif = ft.TextField(
            label="RIF",
            value=self.socio.get("rif", ""),
            border_radius=0,
            border_color=ft.colors.TRANSPARENT,
            bgcolor=Colores.NEGRO,
            focused_border_color=Colores.AMARILLO1,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=17),
            width=180,
            max_length=13,
            hint_text="V121233211",
            on_change=self.validar_rif,
            error_style=ft.TextStyle(color="#FF5733"),
            hover_color=Colores.GRIS00
        )

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
            on_click=lambda _: self.guardar_socio(),
            style=ft.ButtonStyle(
            bgcolor=Colores.AMARILLO1,
            shape=ft.RoundedRectangleBorder(radius=0)
            ),
        )

        self.formulario = ft.Container(
            content=ft.Column([
                ft.Row([self.campo_nombres, self.campo_apellidos], spacing=15),
                ft.Row([self.campo_control, self.campo_cedula, self.campo_fecha, self.campo_telefono], spacing=15),
                ft.Row([self.campo_direccion, self.campo_rif], spacing=15),
                ft.Row([boton_guardar], alignment=ft.MainAxisAlignment.END)
            ]),
            padding=20,
            border_radius=0,
            
        )

    def guardar_socio(self):

        print(f"DEBUG - accion: {self.accion}")
        print(f"DEBUG - id_socio_actual: {self.id_socio_actual}")
        print(f"DEBUG - socio completo: {self.socio}")


        datos_socio = {
            "nombres": self.campo_nombres.value,
            "apellidos": self.campo_apellidos.value,
            "documento": self.campo_cedula.value,
            "numero_telefono": self.campo_telefono.value,
            "numero_control": str(self.campo_control.value),
            "direccion": self.campo_direccion.value,
            "rif": self.campo_rif.value,
            "fecha_nacimiento": self.campo_fecha.value,
        }

        try:
            with httpx.Client() as client:
                if self.accion == "agregar":
                    resp = client.post("http://127.0.0.1:8000/socios/", json=datos_socio)
                else:

                    #print(f"🔍 DEBUG - Actualizando socio con ID: {self.id_socio_actual}")
                    print(f"DEBUG - id_socio_actual: {self.id_socio_actual}")
                    print(f"DEBUG - tipo de id_socio_actual: {type(self.id_socio_actual)}")
                    print(f"DEBUG - datos_socio: {datos_socio}")

                    resp= client.put(f"http://127.0.0.1:8000/socios/{self.id_socio_actual}", json=datos_socio)

                    print(f"DEBUG - Status Code: {resp.status_code}")
                    print(f"DEBUG - Response Text: {resp.text}")

            if resp.status_code in (200, 201):
                # ✅ Refrescamos la tabla en la vista principal
                if hasattr(self.socios_page, 'pagina_view'):
                # Si es SociosTable
                    self.socios_page.pagina_view.tabla.obtener_socio_api()
                    UtilMensajes.mostrar_snack(
                    self.socios_page.pagina_view.page,
                    "Socio guardado correctamente",
                    tipo="success"
                 )
                    self.socios_page.tabla.obtener_socio_api()

                else:
                # Si es SociosView
                    self.socios_page.tabla.obtener_socio_api()
                    UtilMensajes.mostrar_snack(
                    self.socios_page.page,
                    "Socio guardado correctamente", 
                    tipo="success"
                )

            """   UtilMensajes.mostrar_snack(
                    self.socios_page.page,
                    "Socio guardado correctamente",
                    tipo="success"
            )"""

        # Refrescamos la tabla en la vista principal
           # self.socios_page.tabla.obtener_socio_api()

            #UtilMensajes.mostrar_snack(self.socios_page.page, "Socio guardado correctamente", tipo="success")

        # Limpiar campos
            for campo in [
            self.campo_control, self.campo_nombres, self.campo_apellidos,
            self.campo_cedula, self.campo_fecha, self.campo_telefono,
            self.campo_direccion, self.campo_rif,
            ]:
                campo.value = ""
                campo.error_text = None
                campo.update()

        except Exception as err:
        # ✅ CORRECCIÓN: Manejo de errores con la página correcta
            if hasattr(self.socios_page, 'pagina_view'):
                UtilMensajes.mostrar_snack(self.socios_page.pagina_view.page, f"Error al guardar: {err}", tipo="error")
            else:
                UtilMensajes.mostrar_snack(self.socios_page.page, f"Error al guardar: {err}", tipo="error")

    # Validaciones
    def validar_fecha_nacimiento(self, e):
        e.control.error_text = None if Validacion.validar_fecha(e.control.value) else "AAAA-MM-DD"
        e.control.update()

    def validar_cedula(self, e):
        e.control.error_text = None if Validacion.validar_cedula(e.control.value) else "'V-' o 'E-'"
        e.control.update()

    def validar_texto(self, e):
        e.control.error_text = None if Validacion.validar_texto(e.control.value) else "Solo se permiten letras"
        e.control.update()

    def validar_rif(self, e):
        e.control.error_text = None if Validacion.validar_rif(e.control.value) else "Formato RIF inválido"
        e.control.update()


class Validacion:
    @staticmethod
    def validar_fecha(fecha):
        if isinstance(fecha, datetime):
            fecha = fecha.strftime('%Y-%m-%d')
        patron = r'^\d{4}-\d{2}-\d{2}$'
        return re.match(patron, fecha) is not None

    @staticmethod
    def validar_cedula(cedula):
        patron = r'^[VE]-\d{7,9}$'
        return re.match(patron, cedula) is not None

    @staticmethod
    def validar_texto(texto):
        patron = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$'
        return re.match(patron, texto) is not None

    @staticmethod
    def validar_rif(rif):
        patron = r'^[VEJPG]\d{7,10}$'
        return re.match(patron, rif) is not None
