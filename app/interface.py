import flet as ft
import pandas as pd
import os
from get_token.get_access_token import obter_token
from datetime import datetime
from api.consulta import consultar_por_cnpj

def iniciar_app():
    def main(page: ft.Page):
        page.title = "Consulta API JUSBR"
        page.window_width = 650
        page.window_height = 520
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 30
        page.scroll = ft.ScrollMode.AUTO

        file_path_container = {"path": None}
        salvar_em_downloads = ft.Checkbox(
            label="📁 Salvar na pasta de Downloads do sistema",
            value=False,
            tooltip="Se marcado, o arquivo será salvo na sua pasta padrão de Downloads.",
            label_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500)
        )

        texto_ajuda = ft.Text(
            "Se desmarcado, o arquivo será salvo na pasta local ./database",
            size=12,
            italic=True,
            color=ft.colors.GREY_600
        )

        status_text = ft.Text(size=14, selectable=True)
        spinner = ft.ProgressRing(visible=False)

        def on_file_selected(e: ft.FilePickerResultEvent):
            if e.files:
                file_path_container["path"] = e.files[0].path
                status_text.value = f"📄 Arquivo selecionado: {os.path.basename(file_path_container['path'])}"
            else:
                file_path_container["path"] = None
                status_text.value = "⚠️ Nenhum arquivo selecionado."
            page.update()

        file_picker = ft.FilePicker(on_result=on_file_selected)
        page.overlay.append(file_picker)

        def processar(e):
            status_text.value = ""
            spinner.visible = True
            page.update()

            if not file_path_container["path"]:
                status_text.value = "⚠️ Selecione um arquivo .xlsx antes de continuar."
                spinner.visible = False
                page.update()
                return

            try:
                df = pd.read_excel(file_path_container["path"])
                access_token = obter_token()
                resultados = []

                for numero in df['Numero processo'].dropna().astype(str).unique():
                    status_text.value = f"🔍 Consultando: {numero}"
                    page.update()
                    registros = consultar_por_cnpj(numero, access_token)
                    resultados.extend(registros)

                if resultados:
                    df_final = pd.DataFrame(resultados)
                    nome_arquivo = f"resultados_cnpj_{datetime.today().strftime('%Y-%m-%d')}.xlsx"

                    if salvar_em_downloads.value:
                        pasta_saida = os.path.join(os.path.expanduser("~"), "Downloads")
                    else:
                        pasta_saida = os.path.join(os.getcwd(), "database")
                        os.makedirs(pasta_saida, exist_ok=True)

                    caminho_saida = os.path.join(pasta_saida, nome_arquivo)
                    df_final.to_excel(caminho_saida, index=False)

                    status_text.value = f"✅ Consulta finalizada!\n📁 Arquivo salvo em:\n{caminho_saida}"
                else:
                    status_text.value = "⚠️ Nenhum processo retornado."

            except Exception as e:
                status_text.value = f"❌ Erro durante a execução:\n{str(e)}"

            spinner.visible = False
            page.update()

        # Interface
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("📑 Consulta Processual - PDPJ", size=24, weight="bold"),
                    ft.ElevatedButton(
                        text="Selecionar planilha .xlsx",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: file_picker.pick_files(allowed_extensions=["xlsx"]),
                        width=260
                    ),
                    ft.Row([salvar_em_downloads], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([texto_ajuda], alignment=ft.MainAxisAlignment.CENTER),
                    ft.ElevatedButton(
                        text="Iniciar consulta",
                        icon=ft.icons.SEARCH,
                        on_click=processar,
                        width=260,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.BLUE_600,
                            color=ft.colors.WHITE
                        )
                    ),
                    spinner,
                    status_text
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
                ),
                alignment=ft.alignment.center,
                padding=20
            )
        )

    ft.app(target=main)
