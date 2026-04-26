import flet as ft
from utils.colors import Colores
from utils.alerts import UtilMensajes
from auth.auth import AuthControlador
#from datos.datos import datos_finanzas_de_prueba
import httpx
from datetime import datetime
import tempfile
import webbrowser

class FinanzasTable:
    def __init__(self, pagina_view, finanzas=None):
        self.pagina_view = pagina_view
        self._finanzas_original = finanzas
        # Anchos para: Control, Cédula, Pagos, Impuestos, Fecha, Acciones
        self.anchos = [100, 140, 140, 140, 120, 120, 100]
        self.data_table = self._armar_tabla(finanzas)
        self.obtener_finanzas_api()

    def _armar_tabla(self, finanzas):
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
            rows=self._filas(finanzas),
        )

    def _columna(self, texto, ancho):
        estilos = dict(
            weight="w700",
            size=16,
            color=Colores.AMARILLO1,
            font_family="Arial Black italic"
        )
        return ft.DataColumn(
            ft.Container(width=ancho, content=ft.Text(texto, no_wrap=True, **estilos))
        )

    def _columnas(self):
        etiquetas = ["N°","Cédula","Pagos Mensuales","Impuestos Anuales","Fecha de Pago","Numero Control","Acciones"
        ]
        return [self._columna(et, self.anchos[i]) for i, et in enumerate(etiquetas)]

    def _fila(self, registro, index):
        valores = [
            str(index + 1),
            registro["documento"],
            f"{registro['pagos_mensuales']}",
            f"{registro['impuestos_anuales']}",
            registro["fecha_pago"],
            registro["numero_contr"],
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
        acciones = ft.Row(self._botones_accion(registro), alignment="end")
        celdas.append(
            ft.DataCell(
                ft.Container(
                    width=self.anchos[-1],
                    content=acciones
                )
            )
        )
        return ft.DataRow(cells=celdas)

    def _filas(self, finanzas):
        finanzas = finanzas or []
        return [self._fila(f, i) for i, f in enumerate(finanzas)]

    def _botones_accion(self, registro):
        page = self.pagina_view.page
        rol = self.pagina_view.rol
        botones = []
        if rol in ["admin", "user"]:
            botones.append(
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    icon_color="#F4F9FA",
                    on_click=lambda e, r=registro: UtilMensajes.mostrar_sheet(
                        page,
                        "Editar Finanzas",
                        tipo="formulario",
                        vehiculo=None,
                        avance=None,
                        socio=None,
                        sancion=None,
                        finanza=r, vista=self.pagina_view
                    )
                )
            )
        if rol == "admin":
            botones.append(
                ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE,
                    icon_color="#eb3936",
                    on_click=lambda e, r=registro: UtilMensajes.confirmar_material(
                        page=page,
                        titulo="Confirmar Eliminación",
                        mensaje=f"¿Eliminar registro de finanzas {r['numero_contr']}?",
                        on_confirm=lambda e, r=registro: self.eliminar_finanza_api(r),
                        on_cancel=lambda e: print("Eliminación cancelada")
                    )
                )
            )
        return botones

    def obtener_finanzas_api(self):
        try:
            with httpx.Client() as client:
                response = client.get("http://127.0.0.1:8000/finanzas")
                response.raise_for_status()
                self._finanzas_original = response.json()
            self.actualizar(self._finanzas_original)
        except Exception as e:
            print("Error al obtener finanzas:", e)

    def eliminar_finanza_api(self, finanza):
        print(f"Conectando a la API para eliminar la finanza {finanza['id_finanzas']}...")
        try:
            with httpx.Client() as client:
                client.delete(f"http://127.0.0.1:8000/finanzas/{finanza['id_finanzas']}")
        # Actualizamos la tabla
            self._finanzas_original = [f for f in self._finanzas_original if f['id_finanzas'] != finanza['id_finanzas']]
            self.actualizar(self._finanzas_original)
            UtilMensajes.mostrar_snack(self.pagina_view.page, f"Finanza {finanza['id_finanzas']} eliminada", tipo="success")
            print(f"Finanza {finanza['id_finanzas']} eliminada correctamente.")
        except Exception as e:
            UtilMensajes.mostrar_snack(self.pagina_view.page, f"Error al eliminar: {e}", tipo="error")

    def filtrar(self, texto):
        texto = texto.lower()
        filtrados = [
            f for f in self._finanzas_original
            if texto in str(f["numero_contr"]).lower()
            or texto in f["documento"].lower()
            or texto in str(f["pagos_mensuales"])
            or texto in str(f["impuestos_anuales"])
            or texto in f["fecha_pago"].lower()
        ]
        self.actualizar(filtrados)

    def actualizar(self, finanzas):
        self.data_table.rows = self._filas(finanzas)
        if self.data_table.page:  # ✅ evita el error si la tabla aún no está en la vista
            self.data_table.update()


class FinanzasView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.auth = AuthControlador(self.page)
        self.rol = self.auth.obtener_rol()
        self.tabla = FinanzasTable(self)
        self.buscador = ft.TextField(
            label="Buscar finanzas",
            prefix_icon=ft.icons.SEARCH,
            border_radius=0,
            width=500,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=20),
            hint_text="Buscar por control, cédula, fecha...",
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
                    self.page,
                    "Agregar Finanzas",
                    tipo="formulario",
                    finanza=None, vista=self
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
                    on_click=self.generar_pdf_finanzas
                ),
                self._boton_agregar()
            ],
            alignment="start",
            spacing=10
        )

    def generar_pdf_finanzas(self,e):
        try:
        # Llamada al endpoint FastAPI
            with httpx.Client() as client:
                response = client.get("http://127.0.0.1:8000/pdf/finanzas")
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
                    "FINANZAS",
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
        cont_enc = ft.Container(content=encabezado, margin=15)
        cuerpo = ft.Container(content=self.tabla.data_table, expand=True, padding=5)
        scroll = ft.Column(controls=[cuerpo], scroll=ft.ScrollMode.AUTO, expand=True)

        return ft.Column(
            controls=[cont_enc, scroll],
            expand=True,
            alignment=ft.MainAxisAlignment.START
        )


def vista_finanzas(page: ft.Page):
    view = FinanzasView(page)
    return view.construir()