import flet as ft
import pandas as pd
import os
from datetime import datetime
from api.consulta import consultar_por_cnpj


def iniciar_app():
    def main(page: ft.page):
        page.title = "Consulta API JUSBR"
        page.scroll = ft.ScrollMode.AUTO
        page.window_width = 600
        page.window_height = 400


        file_picker = ft.FilePicker()
        status_text = ft.Text(size=14)


        def processar(e):
            status_text.value = ""
            page.update()

            if not file_picker.result:
                status_text.value = "⚠️ Selecione um arquivo .xlsx"
                page.update()
                return

            try:
                file_path = file_p

