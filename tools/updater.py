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

url = query['url']
zip_path = "TwitchMiner.zip"
update_folder = "updates"

if not os.path.exists(update_folder):
    os.makedirs(update_folder)

response = requests.get(url)
with open(zip_path, "wb") as file:
    file.write(response.content)

documents_path = get_documents_path()

with ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(documents_path)

os.remove(zip_path)

print(f"Atualização finalizada, iniciando TwitchMiner.")

miner_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\TwitchMiner.lnk"
try:
    os.startfile(miner_path)
except FileNotFoundError:
    print("Erro: TwitchMiner.exe não foi encontrado.")

sys.exit()
