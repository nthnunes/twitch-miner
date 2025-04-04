import os
import sys
import requests
from zipfile import ZipFile
import ctypes
import ctypes.wintypes
import tkinter as tk
from tkinter import ttk
import threading
import time

def get_documents_path():
    CSIDL_PERSONAL = 5
    SHGFP_TYPE_CURRENT = 0
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    return buf.value

class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TwitchMiner - Instalação")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a1a")
        
        # Centraliza a janela
        window_width = 400
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Título
        self.title_label = tk.Label(
            root, 
            text="TwitchMiner", 
            font=("Segoe UI", 16, "bold"),
            fg="#9147ff",
            bg="#1a1a1a"
        )
        self.title_label.pack(pady=(20, 10))
        
        # Status
        self.status_label = tk.Label(
            root, 
            text="Iniciando instalação...", 
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg="#1a1a1a"
        )
        self.status_label.pack(pady=5)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(
            root, 
            orient="horizontal", 
            length=350, 
            mode="determinate",
            style="TProgressbar"
        )
        self.progress.pack(pady=20)
        
        # Configura estilo da barra de progresso
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TProgressbar", 
                        thickness=20, 
                        troughcolor="#2a2a2a",
                        background="#9147ff")
        
        # Inicia o processo de instalação em uma thread separada
        self.installation_thread = threading.Thread(target=self.install)
        self.installation_thread.daemon = True
        self.installation_thread.start()
    
    def update_status(self, text, progress_value):
        self.status_label.config(text=text)
        self.progress["value"] = progress_value
        self.root.update_idletasks()
    
    def install(self):
        try:
            # Passo 1: Verificando atualizações
            self.update_status("Iniciando instalação...", 10)
            response = requests.get("https://twitch-miner-api.vercel.app/check-update")
            data = response.json()
            url = data["url"]
            zip_path = "TwitchMiner.zip"
            
            # Passo 2: Baixando arquivo
            self.update_status("Baixando arquivos...", 20)
            
            # Download com acompanhamento de progresso
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            # Se o tamanho for conhecido
            if total_size > 0:
                downloaded = 0
                progress_start = 20
                progress_end = 70
                
                with open(zip_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=4096):
                        if chunk:
                            file.write(chunk)
                            downloaded += len(chunk)
                            percent = downloaded / total_size
                            current_progress = progress_start + int(percent * (progress_end - progress_start))
                            self.update_status(f"Baixando... {int(percent * 100)}%", current_progress)
            else:
                # Se o tamanho não for conhecido, baixa normalmente
                with open(zip_path, "wb") as file:
                    file.write(response.content)
                self.update_status("Download concluído", 70)
            
            # Passo 3: Extraindo arquivos
            self.update_status("Extraindo arquivos...", 75)
            documents_path = get_documents_path()
            
            with ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(documents_path)
            
            self.update_status("Finalizando instalação...", 90)
            
            # Passo 4: Limpando arquivos temporários
            os.remove(zip_path)
            
            self.update_status("Instalação concluída!", 100)
            time.sleep(1)
            
            # Passo 5: Iniciando o programa
            miner_exe_path = os.path.join(documents_path, "TwitchMiner", "TwitchMiner.exe")
            try:
                os.startfile(miner_exe_path)
            except FileNotFoundError:
                self.update_status("Erro: Não foi possível iniciar o programa.", 100)
                time.sleep(3)
            
            # Fecha a janela
            self.root.destroy()
            
        except Exception as e:
            self.update_status(f"Erro: {str(e)}", 0)
            time.sleep(5)
            self.root.destroy()

# Inicia a aplicação
root = tk.Tk()
app = InstallerApp(root)
root.mainloop()

# Finaliza o script após fechar a janela
sys.exit()
