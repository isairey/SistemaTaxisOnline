import flet as ft
from utils.colors import Colores
from utils.alerts import UtilMensajes
from auth.auth import AuthControlador
#from datos.datos import datos_vehiculos_de_prueba  
import httpx
import tempfile
import webbrowser


class VehiculosTable:
    def __init__(self, pagina_view, vehiculos=None):
        self.pagina_view = pagina_view
        self._vehiculos_original = vehiculos or []
        self.anchos = [100, 100, 100, 100, 100, 100, 100, 100]  
        self.data_table = self._armar_tabla_vehiculos(vehiculos)
        self.obtener_vehiculos_api() 

    def _armar_tabla_vehiculos(self, vehiculos):
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
            columns=self._columnas_vehiculos(),
            rows=self._filas_vehiculos(vehiculos or []),
        )

    def _columna_vehiculo(self, texto, ancho):
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

    def _columnas_vehiculos(self):
        etiquetas = ["N°", "Documento", "Control", "Marca", "Modelo", "Año", "Placa", "Acciones"]
        return [self._columna_vehiculo(et, self.anchos[i]) for i, et in enumerate(etiquetas)]

    def _fila_vehiculo(self, vehiculo, index):
        valores = [
            str(index + 1),
            vehiculo["documento"],
            vehiculo["numero_control"],
            vehiculo["marca"],
            vehiculo["modelo"],
            str(vehiculo["ano"]),
            vehiculo["placa"],
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
                            no_wrap=False,
                            weight="bold",
                            font_family="Arial",
                            selectable=True,
                        )
                    )
                )
            )
        # columna de acciones
        acciones = ft.Row(self._botones_accion_vehiculo(vehiculo), alignment="end")
        celdas.append(
            ft.DataCell(
                ft.Container(
                    width=self.anchos[-1],
                    content=acciones
                )
            )
        )
        return ft.DataRow(cells=celdas)

    def _filas_vehiculos(self, vehiculos):
        vehiculos = vehiculos or []
        return [self._fila_vehiculo(v, i) for i, v in enumerate(vehiculos)]

    def _botones_accion_vehiculo(self, vehiculo):
        page = self.pagina_view.page
        rol = self.pagina_view.rol

        botones = []
        if rol in ["admin", "user"]:
            botones.append(
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    icon_color="#F4F9FA",
                    on_click=lambda e, v=vehiculo: UtilMensajes.mostrar_sheet(
                        page, "Editar Vehículo", tipo="formulario", vehiculo=v, accion="editar", vista=self.pagina_view
                    )
                )
            )
        if rol == "admin":
            botones.append(
                ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE,
                    icon_color="#eb3936",
                    on_click=lambda e, v=vehiculo: UtilMensajes.confirmar_material(
                        page=page,
                        titulo="Confirmar Eliminación",
                        mensaje=f"¿Eliminar vehículo {v['numero_control']}?",
                        on_confirm=lambda e, v=vehiculo: self.eliminar_vehiculo_api(v),
                        on_cancel=lambda e: print("Eliminación cancelada")
                    )
                )
            )
        return botones
    
    def obtener_vehiculos_api(self):
        try:
            with httpx.Client() as client:
                response = client.get("http://127.0.0.1:8000/vehiculos")
                response.raise_for_status()
                self._vehiculos_original = response.json()
            self.actualizar_vehiculos(self._vehiculos_original)
        except Exception as e:
            print("Error al obtener vehículos:", e)

    def eliminar_vehiculo_api(self, vehiculo):
        try:
            with httpx.Client() as client:
                client.delete(f"http://127.0.0.1:8000/vehiculos/{vehiculo['id_vehiculo']}")
            # 🔹 Quitamos de la lista
            self._vehiculos_original = [v for v in self._vehiculos_original if v['id_vehiculo'] != vehiculo['id_vehiculo']]
            self.actualizar_vehiculos(self._vehiculos_original)
            UtilMensajes.mostrar_snack(self.pagina_view.page, f"Vehículo {vehiculo['placa']} eliminado", tipo="success")
        except Exception as e:
            UtilMensajes.mostrar_snack(self.pagina_view.page, f"Error al eliminar: {e}", tipo="error")

    def filtrar_vehiculos(self, texto):
        texto = texto.lower()
        filtrados = [
            v for v in self._vehiculos_original
            if texto in str(v["numero_control"]).lower()
            or texto in v["documento"].lower()
            or texto in v["marca"].lower()
            or texto in v["modelo"].lower()
            or texto in v["placa"].lower()
        ]
        self.actualizar_vehiculos(filtrados)

    def actualizar_vehiculos(self, vehiculos):
        self.data_table.rows = self._filas_vehiculos(vehiculos)
        if self.data_table.page:
            self.data_table.update()


class VehiculosView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.auth = AuthControlador(self.page)
        self.rol = self.auth.obtener_rol()
        self.tabla = VehiculosTable(self)
        self.buscador = ft.TextField(
            label="Buscar vehículo",
            prefix_icon=ft.icons.SEARCH,
            border_radius=0,
            width=500,
            label_style=ft.TextStyle(color=Colores.BLANCO, size=20),
            hint_text="Buscar por control, placa, marca...",
            bgcolor=ft.colors.TRANSPARENT,
            on_change=self._al_buscar_vehiculo,
            border_color=ft.colors.TRANSPARENT,
            focused_border_color=Colores.BLANCO,
            hover_color=Colores.AZUL4,
        )

    def _al_buscar_vehiculo(self, e):
        self.tabla.filtrar_vehiculos(self.buscador.value)

    def _boton_agregar_vehiculo(self):
        if self.rol in ["admin", "user"]:
            return ft.IconButton(
                icon=ft.icons.ADD,
                icon_size=40,
                style=ft.ButtonStyle(color="#06F58E"),
                on_click=lambda e: UtilMensajes.mostrar_sheet(
                    self.page, "Agregar Vehículo", tipo="formulario", vehiculo=None, accion="agregar", vista=self
                )
            )
        return ft.Container()

    def _boton_pdf_vehiculos(self):
        return ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.PICTURE_AS_PDF,
                    icon_size=30,
                    icon_color=Colores.AMARILLO1,
                    on_click=self.generar_pdf_vehiculos
                ),
                self._boton_agregar_vehiculo()
            ],
            alignment="start",
            spacing=10
        )
    

    def generar_pdf_vehiculos(self, e):
        try:
        # Llamada al endpoint FastAPI
            with httpx.Client() as client:
                response = client.get("http://127.0.0.1:8000/pdf/vehiculos")
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
                    "VEHÍCULOS",
                    size=30,
                    weight="bold",
                    color=Colores.AMARILLO1,
                    font_family="Arial Black italic"
                ),
                self.buscador,
                self._boton_pdf_vehiculos(),
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
        self.page.update()
        self.tabla.obtener_vehiculos_api()

        return ft.Column(
            controls=[
                cont_encabezado,
                columna_scroll
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START
        )


def vista_vehiculos(page: ft.Page):
    view = VehiculosView(page)
    return view.construir()