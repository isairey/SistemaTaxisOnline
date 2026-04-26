import flet as ft
from utils.colors import Colores
from utils.alerts import UtilMensajes
from auth.auth import AuthControlador
#from datos.datos import datos_avances_de_prueba
import httpx
import webbrowser
import tempfile


class AvancesTable:
    def __init__(self, pagina_view, avances=None):
        self.pagina_view = pagina_view
        self._avances_original = avances
        # Control, Nombre, Apellido, F. Nac., RIF, Cédula Avance, Teléfono, Acciones
        self.anchos = [60, 80, 80, 80, 100, 100, 100, 100, 100]
        self.data_table = self._armar_tabla_avances(avances)
        self.obtener_avances_api()

    def _armar_tabla_avances(self, avances):
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
            columns=self._columnas_avances(),
            rows=self._filas_avances(avances),
        )

    def _columna_avance(self, texto, ancho):
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

    def _columnas_avances(self):
        etiquetas = [
            "N°","Nombre","Apellido","Control","F. Nac.","RIF","Cédula Avance","Teléfono","Acciones"
        ]
        return [
            self._columna_avance(et, self.anchos[i])
            for i, et in enumerate(etiquetas)
        ]

    def _fila_avance(self, avance, index):
        valores = [
            str(index + 1),
            avance["nombre"],
            avance["apellido"],
            avance["numero_control"],
            avance["fecha_nacimiento"],
            avance["rif"],
            avance["documento_avance"],
            avance["numero_telf"],
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
        acciones = ft.Row(self._botones_accion_avance(avance), alignment="end")
        celdas.append(
            ft.DataCell(
                ft.Container(
                    width=self.anchos[-1],
                    content=acciones
                )
            )
        )
        return ft.DataRow(cells=celdas)

    def _filas_avances(self, avances):
        avances = avances or []
        return [self._fila_avance(a, i) for i, a in enumerate(avances)]

    def _botones_accion_avance(self, avance):
        page = self.pagina_view.page
        rol = self.pagina_view.rol
        botones = []

        if rol in ["admin", "user"]:
            botones.append(
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    icon_color="#F4F9FA",
                    on_click=lambda e, a=avance: UtilMensajes.mostrar_sheet(
                        page,
                        "Editar Avance",
                        tipo="formulario",
                        vehiculo=None,
                        socio=None,
                        accion="editar",
                        # pass avance so UtilMensajes can choose AvancesForm
                        avance=a, vista=self.pagina_view
                    )
                )
            )
        if rol == "admin":
            botones.append(
                ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE,
                    icon_color="#eb3936",
                    on_click=lambda e, a=avance: UtilMensajes.confirmar_material(
                        page=page,
                        titulo="Confirmar Eliminación",
                        mensaje=f"¿Eliminar avance {a['numero_control']}?",
                        on_confirm=lambda e, a=avance: self.eliminar_avance_api(a),
                        on_cancel=lambda e: print("Eliminación cancelada")
                    )
                )
            )
        return botones

    def obtener_avances_api(self):
        try:
            with httpx.Client() as client:
                response = client.get("http://127.0.0.1:8000/avances")
                response.raise_for_status()
                self._avances_original = response.json()
            self.actualizar_avances(self._avances_original)
        except httpx.HTTPError as e:
            print(f"Error al obtener avances: {e}")
            UtilMensajes.mostrar_snack(self.pagina_view.page, "Error al obtener avances", tipo="error")
            

    def eliminar_avance_api(self, avance):
        print(f"API: eliminando avance {avance['numero_control']}...")
        try:
            with httpx.Client(base_url="http://127.0.0.1:8000/avances") as client:
                client.delete(f"/{avance['id_avance']}")
            self._avances_original = [a for a in self._avances_original if a['id_avance'] != avance['id_avance']]
            self.actualizar_avances(self._avances_original)
            UtilMensajes.mostrar_snack(self.pagina_view.page, f"Avance {avance['numero_control']} eliminado", tipo="success")
            print(f"Avance {avance['numero_control']} eliminado correctamente.")
        except httpx.HTTPError as e:
            print(f"Error al eliminar avance: {e}")
            UtilMensajes.mostrar_snack(self.pagina_view.page, f"Error al eliminar: {e}", tipo="error")

    def filtrar_avances(self, texto):
        texto = texto.lower()
        filtrados = [
            a for a in self._avances_original
            if texto in str(a["numero_control"]).lower()
            or texto in a["nombre"].lower()
            or texto in a["apellido"].lower()
            or texto in a["rif"].lower()
            or texto in a["documento_avance"].lower()
            or texto in a["numero_telf"].lower()
        ]
        self.actualizar_avances(filtrados)

    def actualizar_avances(self, avances):
        self.data_table.rows = self._filas_avances(avances)
        if self.data_table.page:
            self.data_table.page.update()


class AvancesView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.auth = AuthControlador(self.page)
        self.rol = self.auth.obtener_rol()
        self.tabla = AvancesTable(self)
        self.buscador = ft.TextField(
            label="Buscar avance",
            prefix_icon=ft.icons.SEARCH,
            border_radius=0,
            width=500,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=20),
            hint_text="Buscar por control, nombre, cédula…",
            bgcolor=ft.colors.TRANSPARENT,
            on_change=self._al_buscar_avance,
            border_color=ft.colors.TRANSPARENT,
            focused_border_color=Colores.BLANCO,
            hover_color=Colores.AZUL4,
        )

    def _al_buscar_avance(self, e):
        self.tabla.filtrar_avances(self.buscador.value)

    def _boton_agregar_avance(self):
        if self.rol in ["admin", "user"]:
            return ft.IconButton(
                icon=ft.icons.ADD,
                icon_size=40,
                style=ft.ButtonStyle(color="#06F58E"),
                on_click=lambda e:UtilMensajes.mostrar_sheet(
                    self.page,
                    "Agregar Avance",
                    tipo="formulario", avance=None, accion="agregar", vista=self
                )
            )
        return ft.Container()

    def _boton_pdf_avances(self):
        return ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.PICTURE_AS_PDF,
                    icon_size=30,
                    icon_color=Colores.AMARILLO1,
                    on_click=self.generar_pdf_avances
                ),
                self._boton_agregar_avance()
            ],
            alignment="start",
            spacing=10
        )
    
    def generar_pdf_avances(self, e):
        try:
        # Llamada al endpoint FastAPI
            with httpx.Client() as client:
                response = client.get("http://127.0.0.1:8000/pdf/avances")
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
                    "AVANCES",
                    size=30,
                    weight="bold",
                    color=Colores.AMARILLO1,
                    font_family="Arial Black italic"
                ),
                self.buscador,
                self._boton_pdf_avances(),
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


def vista_avances(page: ft.Page):
    view = AvancesView(page)
    return view.construir()