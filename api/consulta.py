import requests
from datetime import datetime

def consultar_por_cnpj(cnpj: str, access_token: str):
    base_url = "https://portaldeservicos.pdpj.jus.br/api/v2/processos"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    resultados = []
    rodada = 1

    while True:
        params = {
            "numeroProcesso": cnpj,
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
            numero_processo = processo.get("numeroProcesso")
            sigla_tribunal = processo.get("siglaTribunal")
            nivel_sigilo = processo.get("nivelSigilo")
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
                        resultados.append({
                            "numeroProcesso": numero_processo,
                            "siglaTribunal": sigla_tribunal,
                            "nivelSigilo": nivel_sigilo,
                            "classe": classe,
                            "assunto": assunto,
                            "orgaoJulgador": orgao_julgador,
                            "valorAcao": valor_acao,
                            "dataDistribuicao": data_dist,
                            "polo": parte.get("polo"),
                            "tipoParte": parte.get("tipoParte"),
                            "nomeParte": parte.get("nome"),
                            "tipoPessoa": parte.get("tipoPessoa"),
                            "documentoParte": parte.get("documentosPrincipais", [{}])[0].get("numero"),
                            "advogado": rep.get("nome"),
                            "tipoRepresentacao": rep.get("tipoRepresentacao"),
                            "cnpj_consultado": cnpj
                        })

        rodada += 1
        break  # apenas 1 página esperada por númeroProcesso

    print(f"\n✅ Total de partes coletadas: {len(resultados)}\n")
    return resultados
