import flet as ft
from utils.colors import Colores
from utils.alerts import UtilMensajes
from auth.auth import AuthControlador
#from datos.datos import datos_sanciones_de_prueba
import httpx
import tempfile
import webbrowser

class SancionesTable:
    def __init__(self, pagina_view, sanciones=None):
        self.pagina_view = pagina_view
        self._sanciones_original = sanciones
        # Anchos para cada columna: Cédula, Nombre, Apellido, Inicio, Final, Monto, Motivo, Acciones
        self.anchos = [80, 100, 100, 100, 70, 70, 70, 150, 80]
        self.data_table = self._armar_tabla_sanciones(sanciones)
        self.obtener_sancion_api()

    def _armar_tabla_sanciones(self, sanciones):
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
            columns=self._columnas_sanciones(),
            rows=self._filas_sanciones(sanciones),
        )

    def _columna_sancion(self, texto, ancho):
        estilos = dict(
            weight="w700",
            size=16,
            color=Colores.AMARILLO1,
            font_family="Arial Black italic"
        )
        return ft.DataColumn(
            ft.Container(width=ancho, content=ft.Text(texto, no_wrap=True, **estilos))
        )

    def _columnas_sanciones(self):
        etiquetas = [
            "Nº","C.I Socio","Nombre","Apellido","Inicio","Final","Monto","Motivo","Acciones"
        ]
        return [
            self._columna_sancion(et, self.anchos[i])
            for i, et in enumerate(etiquetas)
        ]

    def _fila_sancion(self, sancion, index):
        valores = [
            str(index + 1),
            sancion["documento"],
            sancion["nombre"],
            sancion["apellido"],
            sancion["inicio_sancion"],
            sancion["final_sancion"],
            sancion['monto'],
            sancion["motivo_sancion"]
        ]
        celdas = []
        for i, val in enumerate(valores):
            celdas.append(
                ft.DataCell(
                    ft.Container(
                        width=self.anchos[i],
                        content=ft.Text(
                            val,
                            color=Colores.BLANCO,
                            size=12,
                            weight="bold",
                            font_family="Arial",
                            selectable=True,
                        )
                    )
                )
            )
        acciones = ft.Row(self._botones_accion_sancion(sancion), alignment="end")
        celdas.append(
            ft.DataCell(
                ft.Container(
                    width=self.anchos[-1],
                    content=acciones
                )
            )
        )
        return ft.DataRow(cells=celdas)

    def _filas_sanciones(self, sanciones):
        sanciones = sanciones or []
        return [self._fila_sancion(s,i) for i,s in enumerate(sanciones)]

    def _botones_accion_sancion(self, sancion):
        page = self.pagina_view.page
        rol = self.pagina_view.rol
        botones = []

        if rol in ["admin", "user"]:
            botones.append(
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    icon_color="#F4F9FA",
                    on_click=lambda e, s=sancion: UtilMensajes.mostrar_sheet(
                        page,
                        "Editar Sanción",
                        tipo="formulario",
                        sancion=s, vista=self.pagina_view
                    )
                )
            )
        if rol == "admin":
            botones.append(
                ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE,
                    icon_color="#eb3936",
                    on_click=lambda e, s=sancion: UtilMensajes.confirmar_material(
                        page=page,
                        titulo="Confirmar Eliminación",
                        mensaje=f"¿Eliminar sanción de {s['nombre']} ({s['documento']})?",
                        on_confirm=lambda e, s=sancion: self.eliminar_sancion_api(s),
                        on_cancel=lambda e: print("Eliminación cancelada")
                    )
                )
            )
        return botones
    
    def obtener_sancion_api(self):
        try:
            with httpx.Client() as client:
                response = client.get("http://127.0.0.1:8000/sanciones")
                response.raise_for_status()
                self._sanciones_original = response.json()
            self.actualizar_sanciones(self._sanciones_original)
        except Exception as e:
            print("Error al obtener sanciones:", e)

    def eliminar_sancion_api(self, sancion):
        print(f"Conectando a la API para eliminar la sanción de {sancion['documento']}...")
        try:
            with httpx.Client() as client:
                client.delete(f"http://127.0.0.1:8000/sanciones/{sancion['id_sancion']}")
        # Actualizamos la tabla
            self._sanciones_original = [s for s in self._sanciones_original if s['id_sancion'] != sancion['id_sancion']]
            self.actualizar_sanciones(self._sanciones_original)
            UtilMensajes.mostrar_snack(self.pagina_view.page, f"Sanción de {sancion['documento']} eliminada", tipo="success")
            print(f"Sanción de {sancion['documento']} eliminada correctamente.")
        except Exception as e:
            UtilMensajes.mostrar_snack(self.pagina_view.page, f"Error al eliminar: {e}", tipo="error")


    def filtrar_sanciones(self, texto):
        texto = texto.lower()
        filtrados = [
            s for s in self._sanciones_original
            if texto in s["documento"].lower()
            or texto in s["nombre"].lower()
            or texto in s["apellido"].lower()
            or texto in s["inicio_sancion"].lower()
            or texto in s["final_sancion"].lower()
            or texto in str(s["monto"])
            or texto in s["motivo_sancion"].lower()
        ]
        self.actualizar_sanciones(filtrados)

    def actualizar_sanciones(self, sanciones):
        self.data_table.rows = self._filas_sanciones(sanciones)
        if self.data_table.page:
            self.data_table.update()


class SancionesView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.auth = AuthControlador(self.page)
        self.rol = self.auth.obtener_rol()
        self.tabla = SancionesTable(self)
        self.buscador = ft.TextField(
            label="Buscar sanción",
            prefix_icon=ft.icons.SEARCH,
            border_radius=0,
            width=500,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=20),
            hint_text="Buscar por cédula, nombre, motivo...",
            bgcolor=ft.colors.TRANSPARENT,
            on_change=self._al_buscar_sancion,
            border_color=ft.colors.TRANSPARENT,
            focused_border_color=Colores.BLANCO,
            hover_color=Colores.AZUL4,
        )

    def _al_buscar_sancion(self, e):
        self.tabla.filtrar_sanciones(self.buscador.value)

    def _boton_agregar_sancion(self):
        if self.rol in ["admin", "user"]:
            return ft.IconButton(
                icon=ft.icons.ADD,
                icon_size=40,
                style=ft.ButtonStyle(color="#06F58E"),
                on_click=lambda e: UtilMensajes.mostrar_sheet(
                    self.page,
                    "Agregar Sanción",
                    tipo="formulario",
                    sancion=None, vista=self
                )
            )
        return ft.Container()

    def _boton_pdf_sanciones(self):
        return ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.PICTURE_AS_PDF,
                    icon_size=30,
                    icon_color=Colores.AMARILLO1,
                    on_click=self.generar_pdf_sanciones
                ),
                self._boton_agregar_sancion()
            ],
            alignment="start",
            spacing=10
        )
    

    def generar_pdf_sanciones(self, e):
        try:
        # Llamada al endpoint FastAPI
            with httpx.Client() as client:
                response = client.get("http://127.0.0.1:8000/pdf/sanciones")
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
                    "SANCIONES",
                    size=30,
                    weight="bold",
                    color=Colores.AMARILLO1,
                    font_family="Arial Black italic"
                ),
                self.buscador,
                self._boton_pdf_sanciones(),
            ],
            alignment="spaceBetween"
        )
        cont_encabezado = ft.Container(content=encabezado, margin=15)
        cuerpo_scroll = ft.Container(content=self.tabla.data_table, expand=True, padding=5)
        columna_scroll = ft.Column(controls=[cuerpo_scroll], scroll=ft.ScrollMode.AUTO, expand=True)

        return ft.Column(
            controls=[cont_encabezado, columna_scroll],
            expand=True,
            alignment=ft.MainAxisAlignment.START
        )

def vista_sanciones(page: ft.Page):
    view = SancionesView(page)
    return view.construir()