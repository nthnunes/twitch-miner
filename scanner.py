import os, sys
import pythoncom
from win32comext.shell import shell
import ctypes.wintypes
import tkinter as tk
from tkinter import messagebox, simpledialog
from window_manager import show_window, hide_window
import requests
import json
from datetime import datetime


def createShortcut(enable=True):
    startup_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\TwitchMiner.lnk"
    programs_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\TwitchMiner.lnk"
    
    # Se estiver desabilitando, remover o atalho da pasta Startup
    if not enable and os.path.exists(startup_path):
        try:
            os.remove(startup_path)
            return True
        except:
            return False
            
    # Se estiver habilitando, criar o atalho
    if enable and not os.path.exists(startup_path):
        try:
            shortcut = pythoncom.CoCreateInstance (
            shell.CLSID_ShellLink,
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_IShellLink
            )
            shortcut.SetPath(sys.executable)
            shortcut.SetDescription("Twitch Miner")
            shortcut.SetIconLocation(sys.executable, 0)

            persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
            persist_file.Save(startup_path, 0)
        except:
            pass
    
    # Sempre criamos o atalho no menu programas se não existir
    if not os.path.exists(programs_path):
        try:
            shortcut = pythoncom.CoCreateInstance (
            shell.CLSID_ShellLink,
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_IShellLink
            )
            shortcut.SetPath(sys.executable)
            shortcut.SetDescription("Twitch Miner")
            shortcut.SetIconLocation(sys.executable, 0)

            persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
            persist_file.Save(programs_path, 0)
        except:
            pass
    
    return os.path.exists(startup_path)

def check_autostart_enabled():
    """Verifica se a inicialização automática está habilitada"""
    startup_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\TwitchMiner.lnk"
    return os.path.exists(startup_path)

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
    username = data.readline().strip()
    data.close()
    
    # Chamada da API para registrar o cliente
    try:
        api_body = {
            "client": os.getlogin(),
            "twitchUsername": username,
            "version": "2.1.1",
            "lastSignIn": datetime.now().isoformat()
        }
        
        requests.post("https://twitch-miner-api.vercel.app/signup-client", json=api_body)
    except Exception as e:
        pass
    
    return username


config_file = "config.json"

def load_config():
    """Carrega as configurações do arquivo JSON"""
    try:
        if os.path.exists(config_file):
            with open(config_file, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            return {}
    except:
        return {}

def save_config(config):
    """Salva as configurações no arquivo JSON"""
    try:
        with open(config_file, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def get_config_value(key, default_value=True):
    """Obtém um valor específico da configuração"""
    config = load_config()
    
    # Se a chave não existir, adiciona ela com o valor padrão
    if key not in config:
        config[key] = default_value
        save_config(config)
    
    return config.get(key, default_value)

def set_config_value(key, value):
    """Define um valor específico na configuração"""
    config = load_config()
    config[key] = value
    return save_config(config)

def load_auto_update():
    """Carrega a configuração de atualização automática"""
    return get_config_value("auto_update", True)

def save_auto_update(value):
    """Salva a configuração de atualização automática"""
    return set_config_value("auto_update", value)

def save_autostart(value):
    """Salva a configuração de inicialização automática"""
    result = set_config_value("autostart", value)
    
    # Cria ou remove o atalho na pasta Startup
    createShortcut(value)
    
    return result

def load_autostart():
    """Carrega a configuração de inicialização automática"""
    return get_config_value("autostart", True)

def load_chat_notifications():
    """Carrega a configuração de notificações do chat"""
    return get_config_value("chat_notifications", True)

def save_chat_notifications(value):
    """Salva a configuração de notificações do chat"""
    return set_config_value("chat_notifications", value)

def load_chat_connected_notifications():
    """Carrega a configuração de notificações de chat conectado"""
    return get_config_value("chat_connected_notifications", False)

def save_chat_connected_notifications(value):
    """Salva a configuração de notificações de chat conectado"""
    return set_config_value("chat_connected_notifications", value)

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

def search_updates(value=False, version="2.1.1", check_only=False):
    """
    Verifica se há atualizações disponíveis.
    
    Args:
        value (bool): Se True, atualiza automaticamente
        version (str): Versão atual do aplicativo
        check_only (bool): Se True, apenas retorna as informações sem executar a atualização
        
    Returns:
        dict: Informações sobre a atualização se check_only=True
    """
    try:
        response = requests.get("https://twitch-miner-api.vercel.app/check-update")
        data = response.json()

        update_info = {
            "has_update": version != data['version'],
            "current_version": version,
            "latest_version": data['version'],
            "description": data.get('description', ''),
        }
        
        # Se estiver apenas verificando, retorna as informações
        if check_only:
            return update_info
            
        # Se houver atualização disponível
        if update_info["has_update"]:
            if value:  # Se atualizações automáticas estiverem ativadas
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
                
        return update_info
    except Exception as e:
        # Em caso de erro, retorna informações básicas
        return {
            "has_update": False,
            "current_version": version,
            "latest_version": "Desconhecida",
            "description": f"Erro ao verificar atualizações: {str(e)}",
            "error": True
        }

def save_theme(is_dark_theme):
    """Salva a configuração de tema"""
    return set_config_value("dark_theme", is_dark_theme)

def load_theme():
    """Carrega a configuração de tema"""
    return get_config_value("dark_theme", True)