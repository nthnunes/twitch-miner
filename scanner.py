import os, sys
import pythoncom
from win32comext.shell import shell
import ctypes.wintypes
import tkinter as tk
from tkinter import messagebox, simpledialog
from window_manager import show_window, hide_window
import requests


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


def connectUsername():
    root = tk.Tk()

    # Propriedades da janela
    window_width = 500
    window_height = 330

    # Aguarda a janela ser completamente inicializada
    root.update_idletasks()

    # Calcula as dimensões da tela e centraliza a janela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Desabilita redimensionamento
    root.resizable(False, False)

    # Oculta a janela principal para usar apenas os diálogos
    root.withdraw()

    try:
        while True:
            # Exibe o diálogo para o usuário inserir o username
            username = simpledialog.askstring("Username", "Seu usuário da Twitch:", parent=root)

            if username is None:  # Caso o usuário clique em "Cancelar" ou feche a janela
                break

            if username.strip():  # Verifica se o input não está vazio
                with open("username.txt", "w") as data:
                    data.write(username)
                messagebox.showinfo("Sucesso", "Username salvo com sucesso!", parent=root)
                break
            else:
                messagebox.showwarning("Aviso", "O campo não pode ficar vazio. Tente novamente.", parent=root)
    finally:
        root.destroy()  # Garante que a janela seja fechada após o uso


def scanStreamers():
    if not os.path.exists('./streamers.txt'):
        with open("streamers.txt", "w") as data:
            pass
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

def show_update_dialog(description):
    root3 = tk.Tk()
    root3.withdraw()
    user_response = messagebox.askyesno(
        "Twitch Miner",
        f"{description}\n\nAtualizar agora?"
    )
    root3.destroy()
    return user_response

def show_no_update_dialog():
    root3 = tk.Tk()
    root3.withdraw()  # Oculta a janela principal
    messagebox.showinfo(
        "Twitch Miner",
        "Não há atualizações disponíveis."
    )
    root3.destroy()

def search_updates(value, version):
    response = requests.get("https://twitch-miner-api.vercel.app/check-update")
    data = response.json()

    if version != data['version']:
        if value:
            os.startfile("updater.exe")
            os._exit(0)
        else:
            user_response = show_update_dialog(f"Versão {data['version']} disponível\n\n{data['description']}")
            if user_response:
                os.startfile("updater.exe")
                os._exit(0)
    else:
        if value == False:
            show_no_update_dialog()