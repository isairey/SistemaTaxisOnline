# utils/helpers.py
import flet as ft
from utils.colors import Colores


class UtilMensajes:
    @staticmethod
    def mostrar_snack(page, texto, tipo="info"):
        if tipo == "error":
            fondo, color = ft.colors.RED_800, ft.colors.WHITE
        elif tipo == "success":
            fondo, color = ft.colors.GREEN, ft.colors.WHITE
        elif tipo == "pdf":
            fondo, color = "#4511ED", ft.colors.WHITE
        else:
            fondo, color = ft.colors.BLUE_GREY, ft.colors.WHITE

        snack = ft.SnackBar(
            content=ft.Text(texto, color=color),
            bgcolor=fondo,
            open=True
        )
        page.open(snack)
        page.update()

    @staticmethod
    def mostrar_sheet(page, titulo, tipo="mensaje", sancion=None, avance=None, finanza=None,vehiculo=None,socio=None, vista=None,accion=None):
        if accion:
            print("Acción:", accion)
        if tipo == "formulario":
            fondo = Colores.AZUL4

            if socio is not None or titulo.startswith("Agregar Socio"):
                from view.socios.formulario_socio import SociosForm
                contenido_form = SociosForm(
                    socios_page=vista,
                    titulo=titulo,
                    accion="agregar" if socio is None else "actualizar",
                    socio=socio
                
                ).formulario

                contenido = ft.Column([
                    ft.Row(
                        controls=[
                            ft.Text(titulo, style=ft.TextStyle(size=20, weight="bold", color=Colores.AMARILLO1)),
                            ft.IconButton(
                                icon=ft.icons.CANCEL,
                                icon_color="#050404",
                                on_click=lambda _: page.close(bs)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(color=Colores.AMARILLO1),
                    contenido_form
                ])

            elif vehiculo is not None or titulo.startswith("Agregar Vehículo"):
                from view.vehiculos.formulario_vehiculo import VehiculosForm
                contenido_form = VehiculosForm(
                    vehiculos_page=vista,
                    titulo=titulo,
                    accion="agregar" if vehiculo is None else "actualizar",
                    vehiculo=vehiculo
                ).formulario

                contenido = ft.Column([
                    ft.Row(
                        controls=[
                            ft.Text(titulo, style=ft.TextStyle(size=20, weight="bold", color=Colores.AMARILLO1)),
                            ft.IconButton(
                                icon=ft.icons.CANCEL,
                                icon_color="#050404",
                                on_click=lambda _: page.close(bs)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(color=Colores.AMARILLO1),
                    contenido_form
                ])

            elif avance is not None or titulo.startswith("Agregar Avance"):
                from view.avances.formulario_avances import AvancesForm
                contenido_form = AvancesForm(
                    avances_page=vista,
                    titulo=titulo,
                    accion="agregar" if avance is None else "actualizar",
                    avance=avance

                ).formulario

                contenido = ft.Column([
                    ft.Row(
                        controls=[
                            ft.Text(titulo, style=ft.TextStyle(size=20, weight="bold", color=Colores.AMARILLO1)),
                            ft.IconButton(
                                icon=ft.icons.CANCEL,
                                icon_color="#050404",
                                on_click=lambda _: page.close(bs)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(color=Colores.AMARILLO1),
                    contenido_form
                ])

            elif sancion is not None or titulo.startswith("Agregar Sanción"):
                from view.sanciones.formulario_sanciones import SancionesForm
                contenido_form = SancionesForm(
                    sanciones_page=vista,
                    titulo=titulo,
                    accion="agregar" if sancion is None else "actualizar",
                    sancion=sancion

                ).formulario

                contenido = ft.Column([
                    ft.Row(
                        controls=[
                            ft.Text(titulo, style=ft.TextStyle(size=20, weight="bold", color=Colores.AMARILLO1)),
                            ft.IconButton(
                                icon=ft.icons.CANCEL,
                                icon_color="#050404",
                                on_click=lambda _: page.close(bs)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(color=Colores.AMARILLO1),
                    contenido_form
                ])

            elif finanza is not None or titulo.startswith("Agregar Finanzas"):
                from view.finanzas.formulario_finanzas import FinanzasForm
                contenido_form = FinanzasForm(
                    finanzas_page=vista,
                    titulo=titulo,
                    accion="agregar" if finanza is None else "actualizar",
                    finanza=finanza
                ).formulario

                contenido = ft.Column([
                    ft.Row(
                        controls=[
                            ft.Text(titulo, style=ft.TextStyle(size=20, weight="bold", color=Colores.AMARILLO1)),
                            ft.IconButton(
                                icon=ft.icons.CANCEL,
                                icon_color="#050404",
                                on_click=lambda _: page.close(bs)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(color=Colores.AMARILLO1),
                    contenido_form
                ])
            else:
        # Caso de seguridad: no se pasó ningún formulario válido
                contenido = ft.Column([
                    ft.Text("No se pudo cargar el formulario", color="red"),
                    ft.ElevatedButton("Cerrar", on_click=lambda _: page.close(bs))
                ])

        else:
            fondo = Colores.AMARILLO1
            contenido = ft.Column(
                tight=True,
                controls=[
                    ft.Text(titulo, color=Colores.BLANCO),
                    ft.ElevatedButton("Cerrar", on_click=lambda _: page.close(bs))
                ]
            )

        def _al_cerrar(e):
            print("SHEET CERRADO")

        bs = ft.BottomSheet(
            on_dismiss=_al_cerrar,
            content=ft.Container(
                padding=20,
                bgcolor=fondo,
                border_radius=None,
                height=400,
                content=contenido
            )
        )
        page.open(bs)
        page.update()


    @staticmethod
    def confirmar_material(page, titulo, mensaje, on_confirm, on_cancel=None, modal=True):
        def _cerrar(e):
            page.close(dialog)

        acciones = [
            ft.Row(
            controls=[
                ft.IconButton(
                icon=ft.Icons.CANCEL,
                icon_color=ft.colors.RED,
                on_click=lambda e: (on_cancel(e) if on_cancel else None, _cerrar(e))
                ),
                ft.IconButton(
                icon=ft.Icons.CHECK_CIRCLE,
                icon_color=ft.colors.GREEN,
                on_click=lambda e: (on_confirm(e), _cerrar(e))
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
        ]
        dialog = ft.AlertDialog(
            title=ft.Text(titulo),
            content=ft.Text(mensaje),
            actions=acciones,
            modal=modal,
            bgcolor=Colores.GRIS,
            shape=ft.RoundedRectangleBorder(radius=0),  
        )
        page.open(dialog)