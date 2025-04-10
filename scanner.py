import os, sys
import pythoncom
from win32comext.shell import shell
import ctypes.wintypes
import tkinter as tk
from tkinter import messagebox, simpledialog
from window_manager import show_window, hide_window
import requests


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
    username = data.readline()
    data.close()
    return username


config_file = "config.dat"
def load_auto_update():
    """Carrega a configuração de atualização automática do arquivo config.dat"""
    try:
        if not os.path.exists(config_file):
            # Cria um novo arquivo com configurações padrão
            with open(config_file, "w") as file:
                file.write("True\nTrue\nTrue\n")  # [auto_update, autostart, dark_theme]
            return True  # Atualizações automáticas habilitadas por padrão
        else:
            with open(config_file, "r") as file:
                lines = file.readlines()
                
            # Se não houver linhas suficientes, assume verdadeiro
            if not lines:
                return True
                
            # Retorna o valor da primeira linha (atualizações automáticas)
            return lines[0].strip() == "True"
    except:
        return True  # Em caso de erro, retorna o valor padrão

def save_auto_update(value):
    """Salva a configuração de atualização automática no arquivo config.dat"""
    try:
        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                lines = file.readlines()
        else:
            lines = []

        if not lines:
            lines = ["True\n", "True\n"]  # Padrão: [auto_update, autostart]
        
        # Atualiza a linha para atualizações automáticas
        lines[0] = "True\n" if value else "False\n"
        
        # Certifica-se de que há pelo menos duas linhas (para autostart)
        if len(lines) < 2:
            lines.append("True\n")

        with open(config_file, "w") as file:
            file.writelines(lines)
        
        return True
    except:
        return False

def save_autostart(value):
    """Salva a configuração de inicialização automática no arquivo config.dat"""
    try:
        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                lines = file.readlines()
        else:
            lines = []
            
        if not lines:
            lines = ["True\n", "True\n"]  # Padrão: [auto_update, autostart]
            
        # Certifica-se de que há pelo menos duas linhas
        if len(lines) < 2:
            lines.append("True\n")
        
        # Atualiza a linha para inicialização automática
        lines[1] = "True\n" if value else "False\n"
        
        with open(config_file, "w") as file:
            file.writelines(lines)
        
        # Cria ou remove o atalho na pasta Startup
        createShortcut(value)
        
        return True
    except:
        return False

def load_autostart():
    """Carrega a configuração de inicialização automática do arquivo config.dat"""
    try:
        if not os.path.exists(config_file):
            with open(config_file, "w") as file:
                file.write("True\nTrue\n")
            return True
        else:
            with open(config_file, "r") as file:
                lines = file.readlines()
                
            if len(lines) < 2:
                return True  # Valor padrão
                
            return lines[1].strip() == "True"
    except:
        return True  # Em caso de erro, retorna o valor padrão

def load_chat_notifications():
    """Carrega a configuração de notificações do chat do arquivo config.dat"""
    try:
        if not os.path.exists(config_file):
            with open(config_file, "w") as file:
                file.write("True\nTrue\nTrue\nTrue\n")  # [auto_update, autostart, dark_theme, chat_notifications]
            return True
        else:
            with open(config_file, "r") as file:
                lines = file.readlines()
                
            # Se não houver linha suficiente para chat_notifications (4ª linha)
            if len(lines) < 4:
                return True  # Valor padrão: habilitado
                
            return lines[3].strip() == "True"
    except:
        return True  # Em caso de erro, retorna o valor padrão

def save_chat_notifications(value):
    """Salva a configuração de notificações do chat no arquivo config.dat"""
    try:
        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                lines = file.readlines()
        else:
            lines = []
        
        # Garante que temos linhas suficientes
        while len(lines) < 4:
            lines.append("True\n")
            
        # Atualiza a linha para notificações de chat (4ª linha)
        lines[3] = "True\n" if value else "False\n"
        
        with open(config_file, "w") as file:
            file.writelines(lines)
        
        return True
    except:
        return False

def load_chat_connected_notifications():
    """Carrega a configuração de notificações de chat conectado do arquivo config.dat"""
    try:
        if not os.path.exists(config_file):
            with open(config_file, "w") as file:
                file.write("True\nTrue\nTrue\nTrue\nTrue\n")  # [auto_update, autostart, dark_theme, chat_notifications, chat_connected_notifications]
            return True
        else:
            with open(config_file, "r") as file:
                lines = file.readlines()
                
            # Se não houver linha suficiente para chat_connected_notifications (5ª linha)
            if len(lines) < 5:
                # Adiciona a linha faltante
                with open(config_file, "a") as file:
                    file.write("True\n")
                return True  # Valor padrão: habilitado
                
            return lines[4].strip() == "True"
    except:
        return True  # Em caso de erro, retorna o valor padrão

def save_chat_connected_notifications(value):
    """Salva a configuração de notificações de chat conectado no arquivo config.dat"""
    try:
        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                lines = file.readlines()
        else:
            lines = []
        
        # Garante que temos linhas suficientes
        while len(lines) < 5:
            lines.append("True\n")
            
        # Atualiza a linha para notificações de chat conectado (5ª linha)
        lines[4] = "True\n" if value else "False\n"
        
        with open(config_file, "w") as file:
            file.writelines(lines)
        
        return True
    except:
        return False

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

def search_updates(value=False, version="2.0.3", check_only=False):
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
    """Salva a configuração de tema no arquivo config.dat"""
    try:
        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                lines = file.readlines()
        else:
            lines = []
        
        # Garante que temos linhas suficientes
        while len(lines) < 3:
            lines.append("True\n")
            
        # Atualiza a linha para o tema (3ª linha)
        lines[2] = "True\n" if is_dark_theme else "False\n"
        
        # Garante que temos uma 4ª linha para chat_notifications se não existir
        if len(lines) < 4:
            lines.append("True\n")  # Notificações habilitadas por padrão
        
        with open(config_file, "w") as file:
            file.writelines(lines)
        
        return True
    except:
        return False

def load_theme():
    """Carrega a configuração de tema do arquivo config.dat"""
    try:
        if not os.path.exists(config_file):
            with open(config_file, "w") as file:
                file.write("True\nTrue\nTrue\nTrue\n")  # [auto_update, autostart, dark_theme, chat_notifications]
            return True
        else:
            with open(config_file, "r") as file:
                lines = file.readlines()
                
            # Se não houver linhas suficientes para o tema (3ª linha)
            if len(lines) < 3:
                return True  # Tema escuro como padrão
                
            return lines[2].strip() == "True"
    except:
        return True  # Em caso de erro, retorna tema escuro como padrão