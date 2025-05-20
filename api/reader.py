import pandas as pd
import time
from datetime import datetime
import os
from api.consulta import consultar_por_cnpj

def retry_consulta(numero: str, access_token: str, tentativas: int = 3):
    for tentativa in range(1, tentativas + 1):
        try:
            return consultar_por_cnpj(numero, access_token)
        except Exception as e:
            if "429" in str(e):
                espera = 5 * tentativa
                print(f"⚠️ Erro 429: aguardando {espera} segundos antes da próxima tentativa ({tentativa}/{tentativas})")
                time.sleep(espera)
            else:
                raise e
    raise Exception(f"❌ Limite de tentativas excedido para: {numero}")

def executar_consulta(access_token: str):
    input_file = "entrada.xlsx"
    data_hoje = datetime.today().strftime("%Y-%m-%d")
    output_file = os.path.join("database", f"resultados_cnpj_{data_hoje}.xlsx")


    try:
        df = pd.read_excel(input_file)
    except FileNotFoundError:
        print(f"❌ Arquivo de entrada não encontrado: {input_file}")
        return

    resultados = []

    for numero in df['Numero processo'].dropna().astype(str).unique():
        try:
            print(f"🔍 Consultando: {numero}")
            registros = retry_consulta(numero, access_token)
            if registros:
                resultados.extend(registros)
        except Exception as e:
            print(f"❌ Erro na consulta para {numero}: {e}")

    if resultados:
        df_resultados = pd.DataFrame(resultados)

        colunas_ordenadas = [
            "polo", "tipoParte", "nomeParte", "tipoPessoa", "sigilosa",
            "representanteNome", "representanteTipo", "representanteCPF", "representanteOAB",
            "numeroProcesso", "siglaTribunal", "valorAcao", "classe", "assunto",
            "dataUltDistribuicao", "orgaoJulgador"
        ]

        if all(col in df_resultados.columns for col in colunas_ordenadas):
            df_resultados = df_resultados[colunas_ordenadas]

        df_resultados.to_excel(output_file, index=False)
        print(f"\n✅ Arquivo gerado com sucesso: {output_file}")
    else:
        print("⚠️ Nenhum resultado retornado.")
