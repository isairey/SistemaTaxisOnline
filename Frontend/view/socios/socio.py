import flet as ft
from utils.colors import Colores
from utils.alerts import UtilMensajes
from datetime import datetime
from auth.auth import AuthControlador
import httpx
import webbrowser
import tempfile


class SociosTable:
    def __init__(self, pagina_view, socios=None):
        self.pagina_view = pagina_view
        self._socios_original = socios
        self.anchos = [20, None, None, 65, 85, None, 77, 70, None, 100] # Anchos para cada columna
        self.data_table = self._armar_tabla(socios)
        self.obtener_socio_api()

    def _armar_tabla(self, socios):
        return ft.DataTable(
            bgcolor=Colores.NEGRO0,
            border_radius=0,
            heading_row_color=Colores.GRIS,
            data_row_color={
                "hovered": Colores.AZUL,
                "selected": Colores.AZUL2
            },
            data_row_min_height=40,
            data_row_max_height=float("inf"),
            heading_row_height=65,
            columns=self._columnas(),
            rows=self._filas(socios),
        )

    def _columna(self, texto, ancho):
        estilos = dict(
            weight="w700",
            size=15,
            color=Colores.AMARILLO1,
            font_family="Arial Black italic"
        )
        return ft.DataColumn(
            ft.Container(
                width=ancho,
                content=ft.Text(texto, no_wrap=True, **estilos)
            )
        )

    def _columnas(self):
        etiquetas = [
            "N°", "Documento", "Nombres", "Apellidos", "Dirección", "Nro. Móvil",
            "Control", "RIF", "F. Nac.", "Acciones"
        ]
        return [self._columna(et, self.anchos[i]) for i, et in enumerate(etiquetas)]

    def _fila(self,socio, index):
        valores = [
            str(index + 1),
            socio["documento"],
            socio["nombres"],
            socio["apellidos"],
            socio["direccion"],
            socio["numero_telefono"],
            socio["numero_control"],
            socio["rif"],
            socio["fecha_nacimiento"],
            ""
        ]
        celdas = []
        for i, val in enumerate(valores[:-1]):
            celdas.append(
                ft.DataCell(
                    ft.Container(
                        width=self.anchos[i],
                        content=ft.Text(
                            val,
                            color=Colores.BLANCO,
                            size=12,
                            no_wrap=False, 
                            weight="bold",
                            font_family="Arial",
                            selectable=True,
                        )
                    )
                )
            )

        acciones = ft.Row(self._botones_accion(socio), alignment="end")
        celdas.append(
            ft.DataCell(
                ft.Container(
                    width=self.anchos[-1],
                    content=acciones
                )
            )
        )
        return ft.DataRow(cells=celdas)

    def _filas(self, socios):
        socios = socios or []
        return [self._fila(s, i) for i, s in enumerate(socios)]

    def _botones_accion(self, socio):
        page = self.pagina_view.page
        rol = self.pagina_view.rol

        botones = []

        if rol in ["admin", "user"]:
            botones.append(
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    icon_color="#F4F9FA",
                    on_click=lambda e, s=socio: UtilMensajes.mostrar_sheet(
                        page, "Editar Socio", tipo="formulario", socio=s, vista=self.pagina_view
                    )
                )
            )

        if rol == "admin":
            botones.append(
                ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE,
                    icon_color="#eb3936",
                    on_click=lambda e, s=socio: UtilMensajes.confirmar_material(
                        page=page,
                        titulo="Confirmar Eliminación",
                        mensaje=f"¿Está seguro de eliminar al socio {s['nombres']}?",
                        on_confirm=lambda e, s=socio: self.eliminar_socio_api(s),
                        on_cancel=lambda e: print("Eliminación cancelada")
                    )
                )
            )

        return botones
    
    def obtener_socio_api(self):
        try:
            with httpx.Client() as client:
                response = client.get("http://127.0.0.1:8000/socios")
                response.raise_for_status()
                self._socios_original = response.json()
            self.actualizar(self._socios_original)
        except Exception as e:
            print("Error al obtener socios:", e)

    def eliminar_socio_api(self, socio):
        print(f"Conectando a la API para eliminar al socio {socio['nombres']}...")
        try:
            with httpx.Client() as client:
                client.delete(f"http://127.0.0.1:8000/socios/{socio['id_socio']}")
        # Actualizamos la tabla
            self._socios_original = [s for s in self._socios_original if s['id_socio'] != socio['id_socio']]
            self.actualizar(self._socios_original)
            UtilMensajes.mostrar_snack(self.pagina_view.page, f"Socio {socio['nombres']} eliminado", tipo="success")
            print(f"Socio {socio['nombres']} eliminado correctamente.")
        except Exception as e:
            UtilMensajes.mostrar_snack(self.pagina_view.page, f"Error al eliminar: {e}", tipo="error")


    def filtrar(self, texto):
        texto = texto.lower()
        filtrados = [
            s for s in self._socios_original
            if texto in s["nombres"].lower()
            or texto in s["apellidos"].lower()
            or texto in s["documento"].lower()
            or texto in str(s["numero_control"]).lower()
            or texto in s["numero_telefono"].lower()
        ]
        self.actualizar(filtrados)

    def actualizar(self, socios):
        self.data_table.rows = self._filas(socios)
        if self.data_table.page:
            self.data_table.update()


class SociosView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.auth = AuthControlador(self.page)
        self.rol = self.auth.obtener_rol()
        self.tabla = SociosTable(self)
        #self.tabla.obtener_socio_api()
        self.buscador = ft.TextField(
            label="Buscar",
            prefix_icon=ft.icons.SEARCH,
            border_radius=0,
            width=500,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=20),
            hint_text="Buscar por nombre, apellido, cédula, control...",
            bgcolor=ft.colors.TRANSPARENT,
            on_change=self._al_buscar,
            border_color=ft.colors.TRANSPARENT,
            focused_border_color=Colores.BLANCO,
            hover_color=Colores.AZUL4,
        )

    def _al_buscar(self, e):
        self.tabla.filtrar(self.buscador.value)

    def _boton_agregar(self):
        if self.rol in ["admin", "user"]:
            return ft.IconButton(
                icon=ft.icons.ADD,
                icon_size=40,
                style=ft.ButtonStyle(color="#06F58E"),
                on_click=lambda e: UtilMensajes.mostrar_sheet(
                    self.page, "Agregar Socio", tipo="formulario", socio=None, vista=self
                )
            )
        return ft.Container()

    def _boton_pdf(self):
        return ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.PICTURE_AS_PDF,
                    icon_size=30,
                    icon_color=Colores.AMARILLO1,
                    on_click=self.generar_pdf_socios
                ),
                self._boton_agregar()
            ],
            alignment="start",
            spacing=10
        )
    

    def generar_pdf_socios(self, e):
        try:
        # Llamada al endpoint FastAPI
            with httpx.Client() as client:
                response = client.get("http://127.0.0.1:8000/pdf/socios")
                response.raise_for_status()
                pdf_bytes = response.content

        # Guardar PDF temporalmente y abrirlo con el lector por defecto
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            tmp_file.write(pdf_bytes)
            tmp_file.close()
            webbrowser.open(tmp_file.name)

            UtilMensajes.mostrar_snack(self.page, "PDF generado y abierto correctamente", tipo="pdf")
        except Exception as ex:
            UtilMensajes.mostrar_snack(self.page, f"Error al generar PDF: {ex}", tipo="error")



    def construir(self):
        encabezado = ft.Row(
            controls=[
                ft.Text(
                    "SOCIOS",
                    size=30,
                    weight="bold",
                    color=Colores.AMARILLO1,
                    font_family="Arial Black italic"
                ),
                self.buscador,
                self._boton_pdf(),
            ],
            alignment="spaceBetween"
        )
        cont_encabezado = ft.Container(
            content=encabezado,
            margin=15,
        )
        cuerpo_scroll = ft.Container(
            content=self.tabla.data_table,
            expand=True,
            padding=5
        )
        columna_scroll = ft.Column(
            controls=[cuerpo_scroll],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        return ft.Column(
            controls=[
                cont_encabezado,
                columna_scroll
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START
        )


def vista_socios(page: ft.Page):
    view = SociosView(page)
    return view.construir()
