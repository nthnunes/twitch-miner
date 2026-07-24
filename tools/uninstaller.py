import os
import sys
import shutil
import ctypes
import ctypes.wintypes
import threading
import time
import tkinter as tk
from tkinter import ttk


def get_documents_path():
    CSIDL_PERSONAL = 5
    SHGFP_TYPE_CURRENT = 0
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    return buf.value


documents_path = get_documents_path()
twitchminer_path = os.path.join(documents_path, "TwitchMiner")
uninstaller_path = os.path.join(twitchminer_path, "desinstalar.exe")


class UninstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TwitchMiner - Desinstalação")
        self.root.geometry("400x220")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a1a")

        window_width = 400
        window_height = 220
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.title_label = tk.Label(
            root,
            text="TwitchMiner",
            font=("Segoe UI", 16, "bold"),
            fg="#9147ff",
            bg="#1a1a1a",
        )
        self.title_label.pack(pady=(20, 10))

        self.status_label = tk.Label(
            root,
            text="Tem certeza de que deseja desinstalar?\nTodos os dados do TwitchMiner serão removidos.",
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg="#1a1a1a",
            justify="center",
        )
        self.status_label.pack(pady=5)

        self.progress = ttk.Progressbar(
            root,
            orient="horizontal",
            length=350,
            mode="determinate",
            style="TProgressbar",
        )

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "TProgressbar",
            thickness=20,
            troughcolor="#2a2a2a",
            background="#9147ff",
        )

        self.button_frame = tk.Frame(root, bg="#1a1a1a")
        self.button_frame.pack(pady=20)

        self.uninstall_button = tk.Button(
            self.button_frame,
            text="Desinstalar",
            font=("Segoe UI", 10, "bold"),
            fg="#ffffff",
            bg="#9147ff",
            activebackground="#772ce8",
            activeforeground="#ffffff",
            relief="flat",
            width=14,
            cursor="hand2",
            command=self.start_uninstall,
        )
        self.uninstall_button.pack(side=tk.LEFT, padx=8)

        self.cancel_button = tk.Button(
            self.button_frame,
            text="Cancelar",
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg="#3a3a3a",
            activebackground="#4a4a4a",
            activeforeground="#ffffff",
            relief="flat",
            width=14,
            cursor="hand2",
            command=self.root.destroy,
        )
        self.cancel_button.pack(side=tk.LEFT, padx=8)

    def update_status(self, text, progress_value):
        self.status_label.config(text=text)
        self.progress["value"] = progress_value
        self.root.update_idletasks()

    def start_uninstall(self):
        self.button_frame.destroy()
        self.progress.pack(pady=20)
        thread = threading.Thread(target=self.uninstall)
        thread.daemon = True
        thread.start()

    def uninstall(self):
        try:
            self.update_status("Desinstalando TwitchMiner, aguarde...", 10)

            items = os.listdir(twitchminer_path) if os.path.exists(twitchminer_path) else []
            total = len(items) if items else 1
            for index, item in enumerate(items, start=1):
                item_path = os.path.join(twitchminer_path, item)
                if item_path != uninstaller_path:
                    try:
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                    except Exception:
                        pass
                self.update_status(
                    "Removendo arquivos...", 10 + int((index / total) * 60)
                )

            self.update_status("Removendo atalhos...", 80)
            user = os.getlogin()
            startup_shortcut_path = f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\TwitchMiner.lnk"
            programs_shortcut_path = f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\TwitchMiner.lnk"

            if os.path.exists(startup_shortcut_path):
                os.remove(startup_shortcut_path)
            if os.path.exists(programs_shortcut_path):
                os.remove(programs_shortcut_path)

            self.update_status(
                "TwitchMiner desinstalado com sucesso!\nApague a pasta TwitchMiner dos seus Documentos para concluir.",
                100,
            )
            time.sleep(1)
            self.show_close_button()
        except Exception as e:
            self.update_status(f"Erro: {str(e)}", 0)
            self.show_close_button()

    def show_close_button(self):
        close_button = tk.Button(
            self.root,
            text="Fechar",
            font=("Segoe UI", 10, "bold"),
            fg="#ffffff",
            bg="#9147ff",
            activebackground="#772ce8",
            activeforeground="#ffffff",
            relief="flat",
            width=14,
            cursor="hand2",
            command=self.root.destroy,
        )
        close_button.pack(pady=10)


root = tk.Tk()
app = UninstallerApp(root)
root.mainloop()

sys.exit()
