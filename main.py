from api.reader import executar_consulta
from dotenv import load_dotenv
import os
from get_token.get_access_token import obter_token


if __name__ == '__main__':
    access_token = obter_token()

    executar_consulta(access_token)
    #sjkdbsnd