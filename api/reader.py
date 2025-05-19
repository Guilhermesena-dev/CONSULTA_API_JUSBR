import pandas as pd
from api.consulta import consultar_por_cnpj

def executar_consulta(acces_token: str):
    input_file ="entrada.xlsx"
    output_file = "resultados_cnpj.xlsx"

    df = pd.read_excel(input_file)
    resultados = []

    for cnpj in df['Numero processo'].dropna().astype(str).unique():
        try:
            registros = consultar_por_cnpj(cnpj, acces_token)
            resultados.extend(registros)
        except Exception as e:
            print("Erro na consulta: ", e)

    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_excel(output_file, index=False)
    print(f"Resultados cnpj cadastrado com sucesso: {output_file}")