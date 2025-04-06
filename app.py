import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import queue
import sys
import customtkinter as ctk
from PIL import Image
import os

# Definição do diretório de ícones
ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
# Cria o diretório de ícones se não existir
os.makedirs(ICON_DIR, exist_ok=True)

class ConsoleApp(ctk.CTk):
    def __init__(self, tray_icon=None):
        super().__init__()
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")  # Modos: "dark", "light"
        ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"
        
        self.title("TwitchMiner")
        self.geometry("800x600")
        self.minsize(800, 600)

        # Configurar as cores padrão
        self.accent_color = "#9147ff"  # Roxo da Twitch
        self.accent_hover = "#7a30f3"  # Roxo mais escuro para hover
        self.neutral_color = ("#e0e0e0", "#3a3a3a")  # Cor neutra para botões secundários
        self.neutral_hover = ("#cacaca", "#4e4e4e")  # Cor hover para botões secundários
        
        self.tray_icon = tray_icon

        # Carregar ícones
        self.load_icons()

        # Barra lateral
        self.create_sidebar()

        # Frame principal para as abas
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Criação das abas
        self.console_frame = self.create_console_tab()
        self.streams_frame = self.create_streams_tab()
        self.user_frame = self.create_user_tab()
        self.account_frame = self.create_account_tab()

        # Mostra a aba do console por padrão
        self.show_tab("console")

        # Fila para redirecionar o stdout
        self.queue = queue.Queue()
        self.create_console_redirect()

        # Esconde a janela ao iniciar
        self.withdraw()

        # Intercepta o evento de fechamento
        self.protocol("WM_DELETE_WINDOW", self.hide_window)

    def load_icons(self):
        """Carrega os ícones para a aplicação ou usa ícones padrão."""
        # Ícones a serem usados, inicializados como None
        self.console_icon = None
        self.streams_icon = None 
        self.user_icon = None
        self.account_icon = None
        
        # Tamanho dos ícones
        icon_size = (28, 28)
        
        # Tenta carregar os ícones (se existirem)
        try:
            console_path = os.path.join(ICON_DIR, "terminal.png") 
            if os.path.exists(console_path):
                self.console_icon = ctk.CTkImage(Image.open(console_path), size=icon_size)
            
            streams_path = os.path.join(ICON_DIR, "broadcast.png")
            if os.path.exists(streams_path):
                self.streams_icon = ctk.CTkImage(Image.open(streams_path), size=icon_size)
            
            user_path = os.path.join(ICON_DIR, "card.png")
            if os.path.exists(user_path):
                self.user_icon = ctk.CTkImage(Image.open(user_path), size=icon_size)
                
            account_path = os.path.join(ICON_DIR, "user.png")
            if os.path.exists(account_path):
                self.account_icon = ctk.CTkImage(Image.open(account_path), size=icon_size)
        except Exception as e:
            print(f"Erro ao carregar ícones: {e}")

    def create_console_redirect(self):
        sys.stdout = self
        sys.stderr = self

    def write(self, message):
        self.queue.put(message)

    def flush(self):
        pass

    def update_console(self):
        while not self.queue.empty():
            try:
                message = self.queue.get_nowait()
                self.console_output.configure(state=tk.NORMAL)
                self.console_output.insert(tk.END, message)
                self.console_output.configure(state=tk.DISABLED)
                self.console_output.see(tk.END)  # Rolagem automática
            except queue.Empty:
                break
        self.after(100, self.update_console)

    def hide_window(self):
        self.withdraw()  # Esconde a janela
        if self.tray_icon:
            self.tray_icon.notify("O Twitch Miner ainda está rodando na bandeja do sistema.")

    def show_window(self):
        self.deiconify()  # Mostra a janela novamente

    def create_sidebar(self):
        """Cria a barra lateral com botões de ícones."""
        sidebar = ctk.CTkFrame(self, width=80, fg_color=("#f2f2f2", "#171717"))
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Container para centralizar os botões verticalmente
        button_container = ctk.CTkFrame(sidebar, fg_color="transparent")
        button_container.pack(expand=True, fill=tk.BOTH, padx=5, pady=20)
        
        # Função para criar botões com ou sem ícones
        def make_button(text, command, icon_image=None):
            button = ctk.CTkButton(
                button_container, 
                text=text, 
                image=icon_image,
                command=command,
                width=70, 
                height=70,
                corner_radius=8,
                hover_color=("#dddddd", "#2d2d2d"),
                fg_color="transparent",  # Sem cor de fundo
                compound="top",  # Texto abaixo do ícone
                border_width=0,  # Sem borda
                text_color=("black", "white")  # Cor do texto adaptável ao tema
            )
            
            return button
        
        # Criando os botões
        console_btn = make_button("Console", lambda: self.show_tab("console"), self.console_icon)
        console_btn.pack(pady=8, fill=tk.X)
        
        streams_btn = make_button("Streams", lambda: self.show_tab("streams"), self.streams_icon)
        streams_btn.pack(pady=8, fill=tk.X)
        
        # Botão de conta com destaque
        account_btn = make_button("Conta", lambda: self.show_tab("account"), self.account_icon)
        account_btn.pack(pady=8, fill=tk.X)

        user_btn = make_button("Planos", lambda: self.show_tab("user"), self.user_icon)
        user_btn.pack(pady=8, fill=tk.X)

    def create_console_tab(self):
        """Cria o conteúdo da aba do console."""
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(fill=tk.BOTH, expand=True)

        # Use a customtkinter textbox with a scrollbar
        self.console_output = ctk.CTkTextbox(
            frame, 
            wrap="word", 
            state=tk.DISABLED, 
            font=("Segoe UI", 12),
            text_color=("black", "white")
        )
        self.console_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        return frame

    def create_streams_tab(self):
        """Cria o conteúdo da aba de streamers."""
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(fill=tk.BOTH, expand=True)

        # Container para manter o conteúdo 
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=20, anchor="nw")

        # Título e instruções
        title_label = ctk.CTkLabel(content_frame, text="Ordem de prioridade:", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10), anchor="w")

        instruction_label = ctk.CTkLabel(content_frame, text="Segure e arraste para alterar as posições da lista.", font=("Arial", 12))
        instruction_label.pack(pady=(0, 10), anchor="w")

        # Container flex para a lista e controles
        flex_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        flex_container.pack(fill=tk.BOTH, expand=True)

        # Frame para a listbox (lado esquerdo)
        list_frame = ctk.CTkFrame(flex_container, fg_color="transparent")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Listbox para exibir streamers (não existe em customtkinter, usaremos tkinter normal)
        listbox = tk.Listbox(
            list_frame, 
            width=30, 
            height=15, 
            bg=("#f0f0f0" if ctk.get_appearance_mode() == "light" else "#212121"), 
            fg=("black" if ctk.get_appearance_mode() == "light" else "white"),
            selectbackground="#9147ff",
            borderwidth=1,
            relief="solid"
        )
        listbox.pack(fill=tk.BOTH, expand=True)

        # Frame para os controles (lado direito)
        controls_frame = ctk.CTkFrame(flex_container, fg_color="transparent")
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 0))

        # Container para entrada de texto
        add_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        add_frame.pack(fill=tk.X, pady=(0, 10))

        # Label para o prefixo do Twitch
        twitch_label = ctk.CTkLabel(add_frame, text="twitch.tv/", font=("Arial", 12))
        twitch_label.pack(side=tk.LEFT, padx=(5, 5))

        # Campo de entrada para adicionar streamer
        entry = ctk.CTkEntry(add_frame, width=150, font=("Arial", 12))
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        # Botão para adicionar streamer
        add_button = ctk.CTkButton(
            controls_frame, 
            text="Adicionar streamer", 
            command=lambda: self.add_streamer(listbox, entry),
            corner_radius=8,
            fg_color=self.accent_color,
            hover_color=self.accent_hover,
            font=("Arial", 12)
        )
        add_button.pack(fill=tk.X, pady=(0, 10), padx=5)

        # Botão para remover streamer
        remove_button = ctk.CTkButton(
            controls_frame, 
            text="Remover selecionado", 
            command=lambda: self.remove_streamer(listbox),
            corner_radius=8,
            fg_color=self.neutral_color,
            hover_color=self.neutral_hover,
            text_color=("black", "white"),
            font=("Arial", 12)
        )
        remove_button.pack(fill=tk.X, pady=(0, 10), padx=5)

        # Botão para aplicar alterações
        restart_button = ctk.CTkButton(
            controls_frame, 
            text="Aplicar alterações", 
            command=lambda: self.restart_bot(),
            corner_radius=8,
            fg_color=self.neutral_color,
            hover_color=self.neutral_hover,
            text_color=("black", "white"),
            font=("Arial", 12)
        )
        restart_button.pack(fill=tk.X, pady=(0, 10), padx=5)

        # Vincular eventos de arrastar e soltar
        listbox.bind("<Button-1>", lambda event: self.start_drag(event, listbox))
        listbox.bind("<B1-Motion>", lambda event: self.on_drag(event, listbox))

        # Inicializa os streamers na Listbox
        self.refresh_listbox(listbox)

        return frame

    def create_user_tab(self):
        """Cria o conteúdo da aba de planos."""
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(fill=tk.BOTH, expand=True)

        # Container para manter o conteúdo
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=20, anchor="nw")

        # Título
        title_label = ctk.CTkLabel(content_frame, text="Planos Disponíveis", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10), anchor="w")
        
        # Plano Free
        free_frame = ctk.CTkFrame(content_frame, corner_radius=10, border_width=1)
        free_frame.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        free_label = ctk.CTkLabel(free_frame, text="Plano Free (Atual)", font=("Arial", 14, "bold"))
        free_label.pack(anchor="w", padx=15, pady=(15, 0))
        
        free_features = [
            "✓ Mineração automática de pontos",
            "✓ Mineração executada no seu computador",
            "⚠️ Alto uso de CPU",
            "⚠️ Necessário manter o PC ligado"
        ]
        
        for feature in free_features:
            feature_label = ctk.CTkLabel(free_frame, text=feature, font=("Arial", 11), justify=tk.LEFT)
            feature_label.pack(anchor="w", pady=2, padx=15)
            
        # Espaçamento final no frame (reduzido)
        ctk.CTkLabel(free_frame, text="").pack(pady=2)
        
        # Plano Pro
        pro_frame = ctk.CTkFrame(content_frame, corner_radius=10, border_width=1)
        pro_frame.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        pro_label = ctk.CTkLabel(pro_frame, text="Plano Pro", font=("Arial", 14, "bold"))
        pro_label.pack(anchor="w", padx=15, pady=(15, 0))
        
        price_label = ctk.CTkLabel(pro_frame, text="R$ 10,00 / mês", font=("Arial", 12, "bold"), text_color="#9147ff")
        price_label.pack(anchor="w", pady=(5, 10), padx=15)
        
        pro_features = [
            "✓ Mineração em nuvem 24/7",
            "✓ Não precisa manter o PC ligado",
            "✓ Baixo consumo de CPU",
            "✓ Suporte prioritário"
        ]
        
        for feature in pro_features:
            feature_label = ctk.CTkLabel(pro_frame, text=feature, font=("Arial", 11), justify=tk.LEFT)
            feature_label.pack(anchor="w", pady=2, padx=15)
            
        # Espaçamento final no frame (reduzido)
        ctk.CTkLabel(pro_frame, text="").pack(pady=2)
        
        # Função para abrir o chat do Telegram
        def open_telegram_chat():
            import webbrowser
            webbrowser.open("https://t.me/nthnuness")
        
        # Botão para assinar o plano Pro
        subscribe_button = ctk.CTkButton(
            content_frame,
            text="Assinar Plano Pro",
            font=("Arial", 12, "bold"),
            fg_color=self.accent_color,
            hover_color=self.accent_hover,
            corner_radius=8,
            height=50,
            command=open_telegram_chat
        )
        subscribe_button.pack(pady=(10, 0))
        
        return frame
    
    def create_account_tab(self):
        """Cria o conteúdo da aba de conta Twitch."""
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(fill=tk.BOTH, expand=True)

        # Container para manter o conteúdo alinhado à esquerda
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=20, anchor="nw")

        # Rótulo para exibir o nome atual
        title_label = ctk.CTkLabel(content_frame, text="Alterar conta Twitch", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10), anchor="w")

        # Campo para entrada do nome de usuário
        username_label = ctk.CTkLabel(content_frame, text="Nome de usuário atual:", font=("Arial", 12))
        username_label.pack(pady=(5, 10), anchor="w")

        # Exibe o nome atual
        current_username = self.load_username()
        username_entry = ctk.CTkEntry(content_frame, width=300, font=("Arial", 12))
        username_entry.pack(pady=(5, 10), anchor="w")
        username_entry.insert(0, current_username)

        # Botão para salvar o novo nome de usuário
        change_button = ctk.CTkButton(
            content_frame,
            text="Alterar conta Twitch",
            font=("Arial", 12),
            command=lambda: self.change_username(username_entry.get()),
            corner_radius=8,
            fg_color=self.accent_color,
            hover_color=self.accent_hover
        )
        change_button.pack(pady=(10, 10), anchor="w")

        # Texto de observação
        obs_label = ctk.CTkLabel(
            content_frame,
            text=(
                "Observação: Ao alterar seu nome de usuário na Twitch, o bot será reiniciado, "
                "e você precisará fazer login com o novo usuário."
            ),
            font=("Arial", 10),
            wraplength=500,
            justify="left",
        )
        obs_label.pack(pady=(5, 10), anchor="w")

        return frame

    def show_tab(self, tab_name):
        """Alterna entre as abas do console e dos streams."""
        # Esconde todas as abas primeiro
        self.console_frame.pack_forget()
        self.streams_frame.pack_forget()
        self.user_frame.pack_forget()
        self.account_frame.pack_forget()
        
        # Mostra a aba selecionada
        if tab_name == "console":
            self.console_frame.pack(fill=tk.BOTH, expand=True)
        elif tab_name == "streams":
            self.streams_frame.pack(fill=tk.BOTH, expand=True)
        elif tab_name == "user":
            self.user_frame.pack(fill=tk.BOTH, expand=True)
        elif tab_name == "account":
            self.account_frame.pack(fill=tk.BOTH, expand=True)

    def refresh_listbox(self, listbox):
        """Atualiza o Listbox com os streamers do arquivo e adiciona números das posições."""
        try:
            with open("streamers.txt", "r") as file:
                streamers = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            streamers = []

        listbox.delete(0, tk.END)
        for index, streamer in enumerate(streamers, start=1):
            listbox.insert(tk.END, f"{index}. {streamer}")

    def add_streamer(self, listbox, entry):
        """Adiciona um streamer ao arquivo e atualiza o Listbox."""
        streamer = entry.get().strip()
        if streamer:
            current_items = listbox.get(0, tk.END)
            listbox.insert(tk.END, f"{len(current_items) + 1}. {streamer}")
            entry.delete(0, tk.END)
            self.save_streamers(listbox.get(0, tk.END))  # Passa todos os itens do Listbox

    def remove_streamer(self, listbox):
        """Remove o streamer selecionado e atualiza o Listbox."""
        try:
            selected_index = listbox.curselection()[0]
            listbox.delete(selected_index)
            items = listbox.get(0, tk.END)
            listbox.delete(0, tk.END)
            for index, item in enumerate(items, start=1):
                listbox.insert(tk.END, f"{index}. {item.split('. ', 1)[1]}")  # Remove números antigos
            self.save_streamers(listbox.get(0, tk.END))
        except IndexError:
            print("Nenhum streamer selecionado para remoção.")


    def save_streamers(self, items):
        """Salva os streamers no arquivo sem a numeração."""
        with open("streamers.txt", "w") as file:
            for item in items:
                # Remove a numeração ao salvar no arquivo
                streamer_name = item.split(". ", 1)[1]
                file.write(f"{streamer_name}\n")

    # Function to handle the start of a drag
    def start_drag(self, event, listbox):
        global drag_data
        drag_data = {"index": listbox.nearest(event.y)}

    def on_drag(self, event, listbox):
        nearest_index = listbox.nearest(event.y)
        if nearest_index != drag_data["index"]:
            # Atualiza a ordem na lista
            items = list(listbox.get(0, tk.END))
            dragged_item = items[drag_data["index"]]
            items.pop(drag_data["index"])
            items.insert(nearest_index, dragged_item)

            # Atualiza o Listbox com a nova ordem numerada
            listbox.delete(0, tk.END)
            for index, item in enumerate(items, start=1):
                listbox.insert(tk.END, f"{index}. {item.split('. ', 1)[1]}")  # Remove números antigos
            drag_data["index"] = nearest_index

            # Salva os streamers sem a numeração
            self.save_streamers(listbox.get(0, tk.END))


    # Function to simulate restarting the bot
    def restart_bot(self):
        # Exibindo uma mensagem de confirmação
        tk.messagebox.showinfo("Alteração bem-sucedida", f"Para as alterações surtirem efeito reinicie o bot.")

    # Função para carregar o nome de usuário do arquivo
    def load_username(self):
        try:
            with open("username.txt", "r") as file:
                return file.readline().strip()
        except FileNotFoundError:
            tk.messagebox.showerror("Erro", "Arquivo 'username.txt' não encontrado.")
            return ""

    # Função para alterar o nome de usuário
    def change_username(self, new_username):
        if new_username.strip():
            # Salva o novo nome de usuário no arquivo
            with open("username.txt", "w") as file:
                file.write(new_username)
            tk.messagebox.showinfo(
                "Alteração de Conta",
                f"Conta alterada para: {new_username}\n\nPara as alterações surtirem efeito reinicie o bot.",
            )
        else:
            tk.messagebox.showwarning("Erro", "O nome de usuário não pode estar vazio.")


if __name__ == "__main__":
    app = ConsoleApp()
    app.update_console()
    app.mainloop()
