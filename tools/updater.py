import os
import sys
import requests
from zipfile import ZipFile
import ctypes
import ctypes.wintypes
from pymongo import MongoClient
import shutil

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

db = dbConnection("twitch-miner", "dwsHS78YuhKzCAXG")
coll = db.get_collection("updates")
query = coll.find_one({'type': 'latest'})

url = query['url']
zip_path = "TwitchMiner_temp.zip"
update_folder = "updates"

if not os.path.exists(update_folder):
    os.makedirs(update_folder)

response = requests.get(url)
with open(zip_path, "wb") as file:
    file.write(response.content)

with ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(update_folder)

documents_path = get_documents_path()

def copy_with_ignore(src, dest):
    if os.path.basename(src).lower() == "updater.exe":
        return
    if os.path.isdir(src):
        if not os.path.exists(dest):
            os.makedirs(dest)
        for root, dirs, files in os.walk(src):
            relative_path = os.path.relpath(root, src)
            dest_dir = os.path.join(dest, relative_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            for file in files:
                if file.lower() == "updater.exe":
                    continue
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, file)
                shutil.copy2(src_file, dest_file)
    else:
        shutil.copy2(src, dest)

for item in os.listdir(update_folder):
    source = os.path.join(update_folder, item)
    destination = os.path.join(documents_path, item)
    copy_with_ignore(source, destination)

os.remove(zip_path)

print("Atualização finalizada, iniciando TwitchMiner.")

miner_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\TwitchMiner.lnk"
try:
    os.startfile(miner_path)
except FileNotFoundError:
    print("Erro: TwitchMiner.exe não foi encontrado.")

sys.exit()
