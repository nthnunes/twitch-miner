import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import queue
import sys

class ConsoleApp(tk.Tk):
    def __init__(self, tray_icon=None):
        super().__init__()
        self.title("TwitchMiner")
        self.geometry("800x600")

        self.tray_icon = tray_icon

        # Barra lateral
        self.create_sidebar()

        # Frame principal para as abas
        self.main_frame = tk.Frame(self)
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
                self.console_output.config(state=tk.NORMAL)
                self.console_output.insert(tk.END, message)
                self.console_output.config(state=tk.DISABLED)
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
        sidebar = tk.Frame(self, width=80, bg="#f0f0f0")
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Função para criar botões com ou sem ícones
        def make_button(text, command, icon_path=None):
            if icon_path:
                try:
                    # Tenta carregar o ícone
                    icon = tk.PhotoImage(file=icon_path)
                    icon = icon.subsample(16, 16)  # Redimensiona
                    button = tk.Button(
                        sidebar, text=text, image=icon, compound=tk.TOP,
                        command=command, bg="#f0f0f0", relief=tk.FLAT, 
                        width=70, height=60
                    )
                    # Guarda a referência da imagem no botão
                    button.icon = icon
                except Exception as e:
                    print(f"Erro ao carregar ícone {icon_path}: {e}")
                    # Cria botão sem ícone em caso de falha
                    button = tk.Button(
                        sidebar, text=text, command=command,
                        bg="#f0f0f0", relief=tk.FLAT, width=10, height=2
                    )
            else:
                # Cria botão sem ícone
                button = tk.Button(
                    sidebar, text=text, command=command,
                    bg="#f0f0f0", relief=tk.FLAT, width=10, height=2
                )
            
            return button
        
        # Criando os botões
        console_btn = make_button("Console", lambda: self.show_tab("console"), "icons/terminal.png")
        console_btn.pack(padx=5, pady=5, fill=tk.X)
        
        streams_btn = make_button("Streams", lambda: self.show_tab("streams"), "icons/streams.png")
        streams_btn.pack(padx=5, pady=5, fill=tk.X)
        
        # Botão de conta com destaque
        account_btn = make_button("Conta", lambda: self.show_tab("account"), "icons/user.png")
        account_btn.pack(padx=5, pady=5, fill=tk.X)

        user_btn = make_button("Planos", lambda: self.show_tab("user"), "icons/card.png")
        user_btn.pack(padx=5, pady=5, fill=tk.X)

    def create_console_tab(self):
        """Cria o conteúdo da aba do console."""
        frame = tk.Frame(self.main_frame)
        frame.pack(fill=tk.BOTH, expand=True)

        self.console_output = ScrolledText(
            frame, wrap=tk.WORD, state=tk.DISABLED, font=("Segoe UI Emoji", 10)
        )
        self.console_output.pack(fill=tk.BOTH, expand=True)

        return frame

    def create_streams_tab(self):
        """Cria o conteúdo da aba de streamers."""
        frame = tk.Frame(self.main_frame)
        frame.pack(padx=50, pady=50)

        # Título e instruções
        title_label = tk.Label(frame, text="Ordem de prioridade:", font=("Arial", 12, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 1), sticky="w")

        instruction_label = tk.Label(frame, text="Segure e arraste para alterar as posições da lista.", font=("Arial", 8))
        instruction_label.grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky="w")

        # Listbox para exibir streamers
        listbox = tk.Listbox(frame, width=40, height=15)
        listbox.grid(row=2, column=0, rowspan=6, padx=(0, 10), pady=5)

        # Label para o prefixo do Twitch
        twitch_label = tk.Label(frame, text="twitch.tv/", font=("Arial", 10))
        twitch_label.grid(row=2, column=1, sticky="e")

        # Campo de entrada para adicionar streamer
        entry = tk.Entry(frame, width=25)
        entry.grid(row=2, column=2, pady=(5, 0), sticky="w")

        # Botões de funcionalidade
        add_button = tk.Button(frame, text="Adicionar streamer", command=lambda: self.add_streamer(listbox, entry))
        add_button.grid(row=3, column=1, columnspan=2, pady=(0, 70), sticky="ew")

        remove_button = tk.Button(frame, text="Remover selecionado", command=lambda: self.remove_streamer(listbox))
        remove_button.grid(row=4, column=1, columnspan=2, pady=5, sticky="ew")

        restart_button = tk.Button(frame, text="Aplicar alterações", command=lambda: self.restart_bot())
        restart_button.grid(row=5, column=1, columnspan=2, pady=5, sticky="ew")

        # Vincular eventos de arrastar e soltar
        listbox.bind("<Button-1>", lambda event: self.start_drag(event, listbox))
        listbox.bind("<B1-Motion>", lambda event: self.on_drag(event, listbox))

        # Inicializa os streamers na Listbox
        self.refresh_listbox(listbox)

        return frame

    def create_user_tab(self):
        """Cria o conteúdo da aba de planos."""
        frame = tk.Frame(self.main_frame)
        frame.pack(fill=tk.BOTH, expand=True)

        # Container para todo o conteúdo
        content_frame = tk.Frame(frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        title_label = tk.Label(content_frame, text="Planos Disponíveis", font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Plano Free
        free_frame = tk.Frame(content_frame, relief=tk.RIDGE, bd=2, padx=15, pady=15)
        free_frame.pack(fill=tk.X, pady=(0, 15))
        
        free_label = tk.Label(free_frame, text="Plano Free (Atual)", font=("Arial", 14, "bold"))
        free_label.pack(anchor="w")
        
        free_status = tk.Label(free_frame, text="✓ Ativo", font=("Arial", 12), fg="green")
        free_status.pack(anchor="w", pady=(5, 10))
        
        free_features = [
            "✓ Mineração automática de pontos",
            "✓ Mineração executada no seu computador",
            "⚠️ Alto uso de CPU",
            "⚠️ Necessário manter o PC ligado"
        ]
        
        for feature in free_features:
            feature_label = tk.Label(free_frame, text=feature, font=("Arial", 11), justify=tk.LEFT)
            feature_label.pack(anchor="w", pady=2)
        
        # Plano Pro
        pro_frame = tk.Frame(content_frame, relief=tk.RIDGE, bd=2, bg="#f5f5f5", padx=15, pady=15)
        pro_frame.pack(fill=tk.X, pady=(0, 15))
        
        pro_label = tk.Label(pro_frame, text="Plano Pro", font=("Arial", 14, "bold"), bg="#f5f5f5")
        pro_label.pack(anchor="w")
        
        price_label = tk.Label(pro_frame, text="R$ 10,00 / mês", font=("Arial", 12, "bold"), fg="#0066cc", bg="#f5f5f5")
        price_label.pack(anchor="w", pady=(5, 10))
        
        pro_features = [
            "✓ Mineração em nuvem 24/7",
            "✓ Não precisa manter o PC ligado",
            "✓ Baixo consumo de CPU",
            "✓ Suporte prioritário",
            "✓ Relatórios detalhados de ganhos"
        ]
        
        for feature in pro_features:
            feature_label = tk.Label(pro_frame, text=feature, font=("Arial", 11), justify=tk.LEFT, bg="#f5f5f5")
            feature_label.pack(anchor="w", pady=2)
        
        # Função para abrir o chat do Telegram
        def open_telegram_chat():
            import webbrowser
            webbrowser.open("https://t.me/nthnuness")
        
        # Botão para assinar o plano Pro
        subscribe_button = tk.Button(
            content_frame,
            text="Assinar Plano Pro",
            font=("Arial", 12, "bold"),
            bg="#0066cc",
            fg="white",
            padx=15,
            pady=15,
            cursor="hand2",
            command=open_telegram_chat,
            height=2
        )
        subscribe_button.pack(pady=(10, 0))
        
        return frame
    
    def create_account_tab(self):
        """Cria o conteúdo da aba de conta Twitch."""
        frame = tk.Frame(self.main_frame)
        frame.pack(fill=tk.BOTH, expand=True)

        # Container para manter o conteúdo alinhado à esquerda
        content_frame = tk.Frame(frame)
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=20, anchor="nw")

        # Rótulo para exibir o nome atual
        title_label = tk.Label(content_frame, text="Alterar conta Twitch", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10), anchor="w")

        # Campo para entrada do nome de usuário
        username_label = tk.Label(content_frame, text="Nome de usuário atual:", font=("Arial", 12))
        username_label.pack(pady=(5, 5), anchor="w")

        # Exibe o nome atual
        current_username = self.load_username()
        username_entry = tk.Entry(content_frame, width=30, font=("Arial", 12))
        username_entry.pack(pady=(5, 10), anchor="w")
        username_entry.insert(0, current_username)

        # Botão para salvar o novo nome de usuário
        change_button = tk.Button(
            content_frame,
            text="Alterar conta Twitch",
            font=("Arial", 12),
            command=lambda: self.change_username(username_entry.get()),
        )
        change_button.pack(pady=(10, 10), anchor="w")

        # Texto de observação
        obs_label = tk.Label(
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
