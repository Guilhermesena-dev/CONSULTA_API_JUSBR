import requests
import pandas as pd
from datetime import datetime

def consultar_por_cnpj(numero_processo: str, access_token: str):
    base_url = "https://portaldeservicos.pdpj.jus.br/api/v2/processos"
    headers = {
        "Authorization": f"Bearer " + access_token
    }

    resultados = []
    rodada = 1

    while True:
        params = {
            "numeroProcesso": numero_processo,
            "size": 100,
            "sort": ["dataHoraUltimaDistribuicao,DESC", "numeroProcesso,DESC"]
        }

        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Erro na consulta: {response.status_code} - {response.text}")

        data = response.json()
        processos = data.get("content", [])
        print(f"📦 Página {rodada} — {len(processos)} processos")

        if not processos:
            break

        for processo in processos:
            numero_proc = processo.get("numeroProcesso")
            sigla_tribunal = processo.get("siglaTribunal")
            tramitacoes = processo.get("tramitacoes", [])

            for tramitacao in tramitacoes:
                classe = tramitacao.get("classe", [{}])[0].get("descricao")
                assunto = tramitacao.get("assunto", [{}])[0].get("descricao")
                orgao_julgador = tramitacao.get("orgaoJulgador", {}).get("nome")
                valor_acao = tramitacao.get("valorAcao")
                data_dist = tramitacao.get("dataHoraUltimaDistribuicao")
                partes = tramitacao.get("partes", [])

                for parte in partes:
                    representantes = parte.get("representantes", []) or [{}]

                    for rep in representantes:
                        # ⚠️ Trata OAB com segurança
                        representante_oab = None
                        if rep.get("oab") and isinstance(rep["oab"], list) and len(rep["oab"]) > 0:
                            oab_info = rep["oab"][0]
                            numero_oab = oab_info.get("numero", "")
                            uf_oab = oab_info.get("uf", "")
                            if numero_oab and uf_oab:
                                representante_oab = f"{numero_oab}/{uf_oab}"

                        resultados.append({
                            "polo": parte.get("polo"),
                            "tipoParte": parte.get("tipoParte"),
                            "nomeParte": parte.get("nome"),
                            "tipoPessoa": parte.get("tipoPessoa"),
                            "sigilosa": parte.get("sigilosa"),
                            "representanteNome": rep.get("nome"),
                            "representanteTipo": rep.get("tipoRepresentacao"),
                            "representanteCPF": (
                                rep.get("cadastroReceitaFederal", [{}])[0].get("numero")
                                if rep.get("cadastroReceitaFederal") else None
                            ),
                            "representanteOAB": representante_oab,
                            "numeroProcesso": numero_proc,
                            "siglaTribunal": sigla_tribunal,
                            "valorAcao": valor_acao,
                            "classe": classe,
                            "assunto": assunto,
                            "dataUltDistribuicao": data_dist,
                            "orgaoJulgador": orgao_julgador
                        })

        rodada += 1
        break  # apenas uma página por númeroProcesso

    df = pd.DataFrame(resultados)

    colunas_ordenadas = [
        "polo", "tipoParte", "nomeParte", "tipoPessoa", "sigilosa",
        "representanteNome", "representanteTipo", "representanteCPF", "representanteOAB",
        "numeroProcesso", "siglaTribunal", "valorAcao", "classe", "assunto",
        "dataUltDistribuicao", "orgaoJulgador"
    ]
    df = df[colunas_ordenadas]

    print(f"\n✅ Total de registros extraídos: {len(df)}")
    return df.to_dict(orient="records")
