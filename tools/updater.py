import os
import sys
import requests
from zipfile import ZipFile
import ctypes
import ctypes.wintypes
import shutil
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

class UpdaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TwitchMiner - Atualização")
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
            text="Iniciando atualização...", 
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
        
        # Inicia o processo de atualização em uma thread separada
        self.update_thread = threading.Thread(target=self.update)
        self.update_thread.daemon = True
        self.update_thread.start()
    
    def update_status(self, text, progress_value):
        self.status_label.config(text=text)
        self.progress["value"] = progress_value
        self.root.update_idletasks()
    
    def update(self):
        try:
            # Passo 1: Verificando atualizações
            self.update_status("Verificando atualizações...", 10)
            response = requests.get("https://twitch-miner-api.vercel.app/check-update")
            data = response.json()
            url = data["url"]
            zip_path = "TwitchMiner_temp.zip"
            update_folder = "updates"
            
            if not os.path.exists(update_folder):
                os.makedirs(update_folder)
            
            # Passo 2: Baixando atualização
            self.update_status("Baixando atualização...", 20)
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            if total_size > 0:
                downloaded = 0
                progress_start = 20
                progress_end = 60
                
                with open(zip_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=4096):
                        if chunk:
                            file.write(chunk)
                            downloaded += len(chunk)
                            percent = downloaded / total_size
                            current_progress = progress_start + int(percent * (progress_end - progress_start))
                            self.update_status(f"Baixando... {int(percent * 100)}%", current_progress)
            else:
                with open(zip_path, "wb") as file:
                    file.write(response.content)
                self.update_status("Download concluído", 60)
            
            # Passo 3: Extraindo arquivos
            self.update_status("Extraindo arquivos...", 70)
            with ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(update_folder)
            
            documents_path = get_documents_path()
            
            # Passo 4: Copiando arquivos
            self.update_status("Atualizando arquivos...", 80)
            
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
            
            # Passo 5: Limpando arquivos temporários
            self.update_status("Finalizando atualização...", 90)
            os.remove(zip_path)
            shutil.rmtree(update_folder, ignore_errors=True)
            
            self.update_status("Atualização concluída!", 100)
            time.sleep(1)
            
            # Passo 6: Iniciando o programa
            miner_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\TwitchMiner.lnk"
            try:
                os.startfile(miner_path)
            except FileNotFoundError:
                self.update_status("Erro: TwitchMiner.exe não foi encontrado.", 100)
                time.sleep(3)
            
            # Fecha a janela
            self.root.destroy()
            
        except Exception as e:
            self.update_status(f"Erro: {str(e)}", 0)
            time.sleep(5)
            self.root.destroy()

# Inicia a aplicação
root = tk.Tk()
app = UpdaterApp(root)
root.mainloop()

# Finaliza o script após fechar a janela
sys.exit()
