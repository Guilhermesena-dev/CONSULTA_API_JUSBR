# 📑 Consulta Processual PDPJ – App em Flet

Aplicação desktop interativa desenvolvida com [Flet](https://flet.dev/) e Python para consulta processual em massa via API pública do **PDPJ** (Plataforma Digital do Poder Judiciário).

O usuário realiza o upload de uma planilha `.xlsx` com os números de processo, e o sistema realiza a consulta, gera um novo arquivo com os dados extraídos e permite salvar na pasta local ou na pasta de Downloads do sistema.

---

## 🖼️ Interface

- Upload de arquivo `.xlsx`
- Consulta automática à API
- Barra de progresso e mensagens de status
- Opção para abrir o último arquivo gerado
- Layout moderno, responsivo e centralizado

---

## 📁 Estrutura do Projeto

```
consulta_api_jusbr/
├── app/
│   └── interface.py           # Interface Flet
├── api/
│   └── consulta.py            # Lógica de consulta via API PDPJ
├── get_token/
│   └── get_access_token.py    # Geração automática do token via Keycloak
├── database/                  # Arquivos Excel gerados localmente
├── entrada.xlsx               # Arquivo de entrada (modelo)
├── main.py                    # Ponto de entrada da aplicação
├── .env                       # Contém as credenciais do usuário
├── requirements.txt
└── README.md
```

---

## ⚙️ Requisitos

- Python 3.10+
- Virtualenv (recomendado)

### 📦 Instalação

```bash
git clone https://github.com/seu-usuario/consulta_api_jusbr.git
cd consulta_api_jusbr
python -m venv venv
venv\Scripts\activate  # ou source venv/bin/activate no Linux/mac
pip install -r requirements.txt
```

### 📄 Crie o arquivo `.env`

```env
USUARIO_PDPJ=seu_usuario
SENHA_PDPJ=sua_senha
```

---

## ▶️ Como executar

```bash
python main.py
```

O app será iniciado como uma **janela gráfica**.

---

## 📤 Como usar

1. Abra o app com `python main.py`
2. Clique em **Selecionar planilha .xlsx**
3. Marque a opção para salvar na pasta Downloads (se desejar)
4. Clique em **Iniciar consulta**
5. Após finalizar, clique em **Abrir último arquivo gerado** para visualização

---

## 📌 Observações

- Os números de processo devem estar na coluna `Numero processo` do Excel
- A API pode retornar erro 429 se muitas requisições forem feitas em sequência
- O token é gerado automaticamente usando as credenciais do `.env`

---

## 🧪 Tecnologias utilizadas

- [Flet](https://flet.dev/) – GUI moderna com Python
- [Requests](https://docs.python-requests.org/) – requisições HTTP
- [Pandas](https://pandas.pydata.org/) – leitura e manipulação de dados
- [Python-dotenv](https://pypi.org/project/python-dotenv/) – gerenciamento seguro do `.env`

---
