import os, sys
import pythoncom
from win32comext.shell import shell
import ctypes.wintypes
import time
from pymongo import MongoClient
import tkinter as tk
from tkinter import messagebox


def createShortcut():
    if not os.path.exists("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\TwitchMiner.lnk"):
        shortcut = pythoncom.CoCreateInstance (
        shell.CLSID_ShellLink,
        None,
        pythoncom.CLSCTX_INPROC_SERVER,
        shell.IID_IShellLink
        )
        shortcut.SetPath (sys.executable)
        shortcut.SetDescription ("Python %s" % sys.version)
        shortcut.SetIconLocation (sys.executable, 0)

        persist_file = shortcut.QueryInterface (pythoncom.IID_IPersistFile)
        persist_file.Save("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\TwitchMiner.lnk", 0)
    
    if not os.path.exists("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\TwitchMiner.lnk"):
        shortcut = pythoncom.CoCreateInstance (
        shell.CLSID_ShellLink,
        None,
        pythoncom.CLSCTX_INPROC_SERVER,
        shell.IID_IShellLink
        )
        shortcut.SetPath (sys.executable)
        shortcut.SetDescription ("Python %s" % sys.version)
        shortcut.SetIconLocation (sys.executable, 0)

        persist_file = shortcut.QueryInterface (pythoncom.IID_IPersistFile)
        persist_file.Save("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\TwitchMiner.lnk", 0)


def scanStreamers():
    if not os.path.exists('./streamers.txt'):
        time.sleep(1)
        num_streamers = int(input("Número de streams que você deseja assistir: "))
        streamers = []

        for i in range(1, num_streamers + 1):
            username = input(f"{i}. Nome de usuário do streamer: ")
            streamers.append(username)

        with open("streamers.txt", "w") as data:
            for streamer in streamers:
                data.write(streamer + "\n")

        return streamers
    else:
        data = open("streamers.txt", "r")
        streamers = data.readlines()
        data.close()
        return streamers
        

def scanUsername():
    CSIDL_PERSONAL = 5       # My Documents
    SHGFP_TYPE_CURRENT = 0   # Get current, not default value

    buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

    original_path = buf.value
    formatted_path = original_path.replace("\\", "\\\\")
    final_path = formatted_path + "\\\\TwitchMiner"
    os.chdir(final_path)
    
    if not os.path.exists('./username.txt'):
        username = input("Seu usuário da Twitch: ")
        data = open("username.txt", "w")
        data.write(username)
        data.close()
        createShortcut()
        return username
    else:
        data = open("username.txt", "r")
        username = data.readline()
        data.close()
        return username


config_file = "config.dat"
def load_auto_update():
    if not os.path.exists(config_file):
        with open(config_file, "w") as file:
            file.write("True")
        return True
    else:
        with open(config_file, "r") as file:
            value = file.readline().strip()
            return value == "True"

def save_auto_update(value):
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            lines = file.readlines()
    else:
        lines = []

    if lines:
        lines[0] = "True\n" if value else "False\n"
    else:
        lines.append("True\n" if value else "False\n")

    with open(config_file, "w") as file:
        file.writelines(lines)


def dbConnection(username, password):
    CONNECTION_STRING = "mongodb+srv://" + username + ":" + password + "@cluster0.bbxnito.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)

    return client.get_database('twitch-miner')

def show_update_dialog(description):
    root = tk.Tk()
    root.withdraw()
    user_response = messagebox.askyesno(
        "Twitch Miner",
        f"{description}\n\nAtualizar agora?"
    )
    root.destroy()
    return user_response

def show_no_update_dialog():
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal
    messagebox.showinfo(
        "Twitch Miner",
        "Não há atualizações disponíveis."
    )
    root.destroy()

def search_updates(value, version):
    db = dbConnection("", "")
    coll = db.get_collection("updates")
    query = coll.find_one({'type': 'latest'})

    if version != query['version']:
        if value:
            os.startfile("updater.exe")
            os._exit(0)
        else:
            user_response = show_update_dialog(f"Versão {query['version']} disponível\n\n{query['description']}")
            if user_response:
                os.startfile("updater.exe")
                os._exit(0)
    else:
        if value == False:
            show_no_update_dialog()