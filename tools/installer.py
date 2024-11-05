import os
import sys
import requests
from zipfile import ZipFile
import ctypes
import ctypes.wintypes
from pymongo import MongoClient

def get_documents_path():
    CSIDL_PERSONAL = 5
    SHGFP_TYPE_CURRENT = 0
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    return buf.value

def dbConnection(username, password):
    CONNECTION_STRING = "mongodb+srv://" + username + ":" + password + "@cluster0.bbxnito.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)

    return client.get_database('twitch-miner')

db = dbConnection("", "")
coll = db.get_collection("updates")
query = coll.find_one({'type': 'latest'})

# URL do arquivo zip a ser baixado
url = query['url']
zip_path = "TwitchMiner.zip"

# Faz o download do arquivo zip no diretório atual
response = requests.get(url)
with open(zip_path, "wb") as file:
    file.write(response.content)

# Define o caminho para extração como o diretório "Documentos" do usuário
documents_path = get_documents_path()

# Extrai o conteúdo do zip na pasta "Documentos"
with ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(documents_path)

# Remove o arquivo zip após a extração
os.remove(zip_path)

print("Instalação finalizada, iniciando TwitchMiner.")

# Caminho para o executável TwitchMiner.exe na pasta "TwitchMiner" em "Documentos"
miner_exe_path = os.path.join(documents_path, "TwitchMiner", "TwitchMiner.exe")
try:
    os.startfile(miner_exe_path)
except FileNotFoundError:
    print("Erro: Ocorreu um erro ao instalar.")

# Finaliza o script
sys.exit()
