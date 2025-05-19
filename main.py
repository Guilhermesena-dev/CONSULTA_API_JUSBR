from api.reader import executar_consulta
from dotenv import load_dotenv
import os
if __name__ == '__main__':
    load_dotenv()
    access_token = os.getenv("ACCESS_TOKEN")

    executar_consulta(access_token)