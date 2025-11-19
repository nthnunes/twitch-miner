import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import queue
import sys
import customtkinter as ctk
from PIL import Image
import os

class ConsoleApp(ctk.CTk):
    def __init__(self, tray_icon=None):
        super().__init__()
        
        # Importa o módulo scanner para carregar as configurações
        try:
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            import scanner
            # Aplica o tema conforme a configuração salva
            is_dark_theme = scanner.load_theme()
            ctk.set_appearance_mode("dark" if is_dark_theme else "light")
        except:
            # Se ocorrer algum erro, usa o tema escuro como padrão
            ctk.set_appearance_mode("dark")
        
        ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"
        
        self.title("TwitchMiner")
        self.geometry("800x600")
        self.minsize(800, 600)
        
        # Define o ícone da janela
        try:
            self.iconbitmap("icons/window.ico")
        except:
            # Se não conseguir carregar o ícone, continua sem ele
            pass
 
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
        self.settings_frame = self.create_settings_tab()
        self.about_frame = self.create_about_tab()

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
        self.about_icon = None
        self.settings_icon = None
        
        # Tamanho dos ícones
        icon_size = (28, 28)
        
        # Tenta carregar os ícones (se existirem)
        try:
            console_path = os.path.join("icons", "terminal.png") 
            if os.path.exists(console_path):
                self.console_icon = ctk.CTkImage(Image.open(console_path), size=icon_size)
            
            streams_path = os.path.join("icons", "streams.png")
            if os.path.exists(streams_path):
                self.streams_icon = ctk.CTkImage(Image.open(streams_path), size=icon_size)
            
            user_path = os.path.join("icons", "puzzle.png")
            if os.path.exists(user_path):
                self.user_icon = ctk.CTkImage(Image.open(user_path), size=icon_size)
                
            account_path = os.path.join("icons", "user.png")
            if os.path.exists(account_path):
                self.account_icon = ctk.CTkImage(Image.open(account_path), size=icon_size)
                
            about_path = os.path.join("icons", "about.png")
            if os.path.exists(about_path):
                self.about_icon = ctk.CTkImage(Image.open(about_path), size=icon_size)
                
            settings_path = os.path.join("icons", "settings.png")
            if os.path.exists(settings_path):
                self.settings_icon = ctk.CTkImage(Image.open(settings_path), size=icon_size)
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

        user_btn = make_button("Addons", lambda: self.show_tab("user"), self.user_icon)
        user_btn.pack(pady=8, fill=tk.X)
        
        settings_btn = make_button("Ajustes", lambda: self.show_tab("settings"), self.settings_icon)
        settings_btn.pack(pady=8, fill=tk.X)
        
        about_btn = make_button("Sobre", lambda: self.show_tab("about"), self.about_icon)
        about_btn.pack(pady=8, fill=tk.X)

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
        
        # Definir cores baseadas no tema atual
        bg_color = "#212121" if ctk.get_appearance_mode().lower() == "dark" else "#f0f0f0"
        fg_color = "white" if ctk.get_appearance_mode().lower() == "dark" else "black"
        
        # Listbox para exibir streamers (não existe em customtkinter, usaremos tkinter normal)
        self.streams_listbox = tk.Listbox(
            list_frame, 
            width=30, 
            height=15, 
            bg=bg_color, 
            fg=fg_color,
            selectbackground="#9147ff",
            borderwidth=1,
            relief="solid"
        )
        self.streams_listbox.pack(fill=tk.BOTH, expand=True)

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
            command=lambda: self.add_streamer(self.streams_listbox, entry),
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
            command=lambda: self.remove_streamer(self.streams_listbox),
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

        # Botão para ver loja StreamElements
        streamelements_button = ctk.CTkButton(
            controls_frame, 
            text="Ver Loja StreamElements", 
            command=lambda: self.open_streamelements_store(self.streams_listbox),
            corner_radius=8,
            fg_color=self.accent_color,
            hover_color=self.accent_hover,
            font=("Arial", 12)
        )
        streamelements_button.pack(fill=tk.X, pady=(40, 10), padx=5)

        # Vincular eventos de arrastar e soltar
        self.streams_listbox.bind("<Button-1>", lambda event: self.start_drag(event, self.streams_listbox))
        self.streams_listbox.bind("<B1-Motion>", lambda event: self.on_drag(event, self.streams_listbox))

        # Inicializa os streamers na Listbox
        self.refresh_listbox(self.streams_listbox)

        return frame

    def create_user_tab(self):
        """Cria o conteúdo da aba de addons."""
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(fill=tk.BOTH, expand=True)

        # Container para manter o conteúdo centralizado
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Centralizar o texto na tela
        center_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill=tk.BOTH)

        # Texto principal centralizado
        message_label = ctk.CTkLabel(
            center_frame, 
            text="Em breve recursos extras para você ganhar ainda mais drops e skins.",
            font=("Arial", 12),
            wraplength=600,
            justify="center"
        )
        message_label.pack(expand=True)
        
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

    def create_about_tab(self):
        """Cria o conteúdo da aba de sobre."""
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(fill=tk.BOTH, expand=True)

        # Container para manter o conteúdo
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(content_frame, text="Sobre o TwitchMiner", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10), anchor="center")
        
        # Versão
        version_label = ctk.CTkLabel(content_frame, text="Versão 2.1.3", font=("Arial", 14))
        version_label.pack(pady=(0, 10), anchor="center")
        
        # Desenvolvedor
        dev_label = ctk.CTkLabel(
            content_frame, 
            text="Desenvolvido por o tal do nunes", 
            font=("Arial", 12)
        )
        dev_label.pack(pady=(0, 30), anchor="center")
        
        # Função para abrir links
        def open_link(url):
            import webbrowser
            webbrowser.open(url)
        
        # Frame para os links (centralizado)
        links_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        links_frame.pack(pady=(0, 20), anchor="center")
        
        # Link para o site
        site_button = ctk.CTkButton(
            links_frame,
            text="Site Oficial",
            font=("Arial", 12),
            fg_color=self.accent_color,
            hover_color=self.accent_hover,
            corner_radius=8,
            width=250,
            command=lambda: open_link("https://twitch-miner-web.vercel.app/")
        )
        site_button.pack(pady=10)
        
        # Link para outras versões
        versions_button = ctk.CTkButton(
            links_frame,
            text="Outras Versões",
            font=("Arial", 12),
            fg_color=self.neutral_color,
            hover_color=self.neutral_hover,
            text_color=("black", "white"),
            corner_radius=8,
            width=250,
            command=lambda: open_link("https://twitch-miner-web.vercel.app/versions")
        )
        versions_button.pack(pady=10)
        
        # Frame para o botão de suporte (alinhado na parte inferior)
        support_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        support_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 10))
        
        # Botão de suporte
        support_button = ctk.CTkButton(
            support_frame,
            text="Falar com Suporte",
            font=("Arial", 12, "bold"),
            fg_color=self.accent_color,
            hover_color=self.accent_hover,
            corner_radius=8,
            height=45,
            command=lambda: open_link("https://t.me/nthnuness")
        )
        support_button.pack(pady=10, padx=20, side=tk.BOTTOM)
        
        return frame

    def create_settings_tab(self):
        """Cria o conteúdo da aba de configurações."""
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(fill=tk.BOTH, expand=True)

        # Cria um frame com scrollbar
        scroll_container = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll_container.pack(fill=tk.BOTH, expand=True)

        # Container para manter o conteúdo
        content_frame = ctk.CTkFrame(scroll_container, fg_color="transparent")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(content_frame, text="Configurações", font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20), anchor="w")
        
        # Frame para configurações de aparência
        appearance_frame = ctk.CTkFrame(content_frame)
        appearance_frame.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        # Título da seção de aparência
        appearance_title = ctk.CTkLabel(
            appearance_frame, 
            text="Aparência", 
            font=("Arial", 14, "bold")
        )
        appearance_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Container para o switch do tema
        theme_container = ctk.CTkFrame(appearance_frame, fg_color="transparent")
        theme_container.pack(fill=tk.X, padx=15, pady=10)
        
        # Label para o tema
        theme_label = ctk.CTkLabel(
            theme_container,
            text="Tema Escuro",
            font=("Arial", 12)
        )
        theme_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Importa as funções do scanner
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        try:
            import scanner
        except ImportError:
            # Em caso de erro, define métodos vazios
            class DummyScanner:
                @staticmethod
                def load_auto_update():
                    return True
                
                @staticmethod
                def save_auto_update(value):
                    return True
                
                @staticmethod
                def check_autostart_enabled():
                    return True
                
                @staticmethod
                def load_autostart():
                    return True
                
                @staticmethod
                def save_autostart(value):
                    return True
                
                @staticmethod
                def save_theme(is_dark_theme):
                    return True
                    
                @staticmethod
                def load_theme():
                    return True
                
                @staticmethod
                def load_chat_notifications():
                    return True
                
                @staticmethod
                def save_chat_notifications(value):
                    return True
                
                @staticmethod
                def load_chat_connected_notifications():
                    return True
                
                @staticmethod
                def save_chat_connected_notifications(value):
                    return True
                
                @staticmethod
                def search_updates(value=False, version="2.1.3", check_only=False):
                    return {
                        "has_update": False,
                        "current_version": "2.1.3",
                        "latest_version": "2.1.3",
                        "description": "",
                        "error": False
                    }
            
            scanner = DummyScanner
        
        # Função para alternar o tema
        def toggle_theme():
            # Obtém o estado atual do switch
            is_dark_theme = theme_switch.get() == 1
            
            # Alterna o tema
            ctk.set_appearance_mode("dark" if is_dark_theme else "light")
            theme_label.configure(text="Tema Escuro" if is_dark_theme else "Tema Claro")
            
            # Salva a preferência
            try:
                scanner.save_theme(is_dark_theme)
            except:
                pass
            
            # Atualiza a cor de fundo da listbox na aba streams
            self.update_listbox_colors()
        
        # Switch para alternar o tema
        theme_switch = ctk.CTkSwitch(
            theme_container,
            text="",
            command=toggle_theme,
            button_color=self.accent_color,
            button_hover_color=self.accent_hover,
            progress_color=self.accent_color
        )
        
        # Define o estado inicial do switch baseado no tema atual
        if ctk.get_appearance_mode().lower() == "dark":
            theme_switch.select()
            theme_label.configure(text="Tema Escuro")
        else:
            theme_switch.deselect()
            theme_label.configure(text="Tema Claro")
            
        theme_switch.pack(side=tk.RIGHT)
        
        # Frame para configurações de notificações
        notifications_frame = ctk.CTkFrame(content_frame)
        notifications_frame.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        # Título da seção de notificações
        notifications_title = ctk.CTkLabel(
            notifications_frame, 
            text="Notificações", 
            font=("Arial", 14, "bold")
        )
        notifications_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Container para o switch de notificações de chat
        chat_notifications_container = ctk.CTkFrame(notifications_frame, fg_color="transparent")
        chat_notifications_container.pack(fill=tk.X, padx=15, pady=10)
        
        # Label para notificações de chat
        chat_notifications_label = ctk.CTkLabel(
            chat_notifications_container,
            text="Menções e Respostas do Chat",
            font=("Arial", 12)
        )
        chat_notifications_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Função para alternar notificações de chat
        def toggle_chat_notifications():
            try:
                state = chat_notifications_switch.get()
                scanner.save_chat_notifications(state == 1)
            except:
                pass
        
        # Switch para alternar notificações de chat
        chat_notifications_switch = ctk.CTkSwitch(
            chat_notifications_container,
            text="",
            command=toggle_chat_notifications,
            button_color=self.accent_color,
            button_hover_color=self.accent_hover,
            progress_color=self.accent_color
        )
        
        # Define o estado inicial do switch baseado na configuração
        try:
            if scanner.load_chat_notifications():
                chat_notifications_switch.select()
            else:
                chat_notifications_switch.deselect()
        except:
            chat_notifications_switch.select()  # Padrão: habilitado
            
        chat_notifications_switch.pack(side=tk.RIGHT)
        
        # Container para o switch de notificações de chat conectado
        chat_connected_notifications_container = ctk.CTkFrame(notifications_frame, fg_color="transparent")
        chat_connected_notifications_container.pack(fill=tk.X, padx=15, pady=10)
        
        # Label para notificações de chat conectado
        chat_connected_notifications_label = ctk.CTkLabel(
            chat_connected_notifications_container,
            text="Chat Conectado",
            font=("Arial", 12)
        )
        chat_connected_notifications_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Função para alternar notificações de chat conectado
        def toggle_chat_connected_notifications():
            try:
                state = chat_connected_notifications_switch.get()
                scanner.save_chat_connected_notifications(state == 1)
            except:
                pass
        
        # Switch para alternar notificações de chat conectado
        chat_connected_notifications_switch = ctk.CTkSwitch(
            chat_connected_notifications_container,
            text="",
            command=toggle_chat_connected_notifications,
            button_color=self.accent_color,
            button_hover_color=self.accent_hover,
            progress_color=self.accent_color
        )
        
        # Define o estado inicial do switch baseado na configuração
        try:
            if scanner.load_chat_connected_notifications():
                chat_connected_notifications_switch.select()
            else:
                chat_connected_notifications_switch.deselect()
        except:
            chat_connected_notifications_switch.select()  # Padrão: habilitado
            
        chat_connected_notifications_switch.pack(side=tk.RIGHT)
        
        # Frame para configurações do sistema
        system_frame = ctk.CTkFrame(content_frame)
        system_frame.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        # Título da seção de sistema
        system_title = ctk.CTkLabel(
            system_frame, 
            text="Sistema", 
            font=("Arial", 14, "bold")
        )
        system_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Container para o switch de atualizações automáticas
        auto_update_container = ctk.CTkFrame(system_frame, fg_color="transparent")
        auto_update_container.pack(fill=tk.X, padx=15, pady=10)
        
        # Label para atualizações automáticas
        auto_update_label = ctk.CTkLabel(
            auto_update_container,
            text="Atualizações Automáticas",
            font=("Arial", 12)
        )
        auto_update_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Função para alternar atualizações automáticas
        def toggle_auto_update():
            try:
                state = auto_update_switch.get()
                scanner.save_auto_update(state == 1)
            except:
                pass
        
        # Switch para alternar atualizações automáticas
        auto_update_switch = ctk.CTkSwitch(
            auto_update_container,
            text="",
            command=toggle_auto_update,
            button_color=self.accent_color,
            button_hover_color=self.accent_hover,
            progress_color=self.accent_color
        )
        
        # Define o estado inicial do switch baseado na configuração
        try:
            if scanner.load_auto_update():
                auto_update_switch.select()
            else:
                auto_update_switch.deselect()
        except:
            auto_update_switch.select()  # Padrão: habilitado
            
        auto_update_switch.pack(side=tk.RIGHT)
        
        # Container para o switch de inicialização automática
        auto_start_container = ctk.CTkFrame(system_frame, fg_color="transparent")
        auto_start_container.pack(fill=tk.X, padx=15, pady=10)
        
        # Label para inicialização automática
        auto_start_label = ctk.CTkLabel(
            auto_start_container,
            text="Iniciar com o Windows",
            font=("Arial", 12)
        )
        auto_start_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Função para alternar inicialização automática
        def toggle_auto_start():
            try:
                state = auto_start_switch.get()
                scanner.save_autostart(state == 1)
            except:
                pass
        
        # Switch para alternar inicialização automática
        auto_start_switch = ctk.CTkSwitch(
            auto_start_container,
            text="",
            command=toggle_auto_start,
            button_color=self.accent_color,
            button_hover_color=self.accent_hover,
            progress_color=self.accent_color
        )
        
        # Define o estado inicial do switch baseado na configuração
        try:
            if scanner.load_autostart():
                auto_start_switch.select()
            else:
                auto_start_switch.deselect()
        except:
            auto_start_switch.select()  # Padrão: habilitado
            
        auto_start_switch.pack(side=tk.RIGHT)
        
        # Frame para o resultado da busca de atualizações
        update_result_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        update_result_frame.pack(fill=tk.X, pady=(5, 15), padx=5)
        
        # Frame horizontal para conter os dois labels lado a lado
        update_text_frame = ctk.CTkFrame(update_result_frame, fg_color="transparent")
        update_text_frame.pack(pady=(5, 0))
        
        # Label para mostrar o status da atualização
        update_status_label = ctk.CTkLabel(
            update_text_frame,
            text="",
            font=("Arial", 12),
            justify="right"
        )
        update_status_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Label clicável para "Atualizar agora"
        update_action_label = ctk.CTkLabel(
            update_text_frame,
            text="",
            font=("Arial", 12, "bold"),
            text_color=self.accent_color,
            cursor="hand2",
            justify="left"
        )
        update_action_label.pack(side=tk.LEFT)
        
        # Versão atual do aplicativo
        VERSION = "2.1.3"
        
        # Função para buscar atualizações
        def check_for_updates():
            try:
                # Altera o texto para "Verificando..."
                update_status_label.configure(text="Verificando atualizações...")
                update_action_label.configure(text="")
                
                # Atualiza a interface
                self.update()
                
                # Busca por atualizações
                result = scanner.search_updates(False, VERSION, True)
                
                # Verifica se houve erro
                if result.get("error", False):
                    update_status_label.configure(
                        text=f"Erro ao verificar atualizações: {result.get('description', 'Erro desconhecido')}",
                        text_color="red"
                    )
                    update_action_label.configure(text="")
                    return
                
                # Se há atualização disponível
                if result["has_update"]:
                    # Configura o texto inicial
                    update_status_label.configure(
                        text=f"Versão {result['latest_version']} disponível.",
                        text_color=("black", "white")
                    )
                    
                    # Configura o texto de ação
                    update_action_label.configure(text="Atualizar agora")
                    
                    # Adiciona evento de clique para iniciar a atualização
                    def start_update(event):
                        try:
                            os.startfile("updater.exe")
                            os._exit(0)
                        except:
                            update_status_label.configure(
                                text="Erro ao iniciar o atualizador.",
                                text_color="red"
                            )
                            update_action_label.configure(text="")
                    
                    # Adiciona o evento de clique ao label
                    update_action_label.bind("<Button-1>", start_update)
                else:
                    update_status_label.configure(
                        text=f"Não há atualizações disponíveis. A versão {result['latest_version']} é a mais recente.",
                        text_color=("black", "white")
                    )
                    update_action_label.configure(text="")
            except Exception as e:
                update_status_label.configure(
                    text=f"Erro ao verificar atualizações: {str(e)}",
                    text_color="red"
                )
                update_action_label.configure(text="")
        
        # Botão para buscar atualizações
        check_updates_button = ctk.CTkButton(
            content_frame,
            text="Buscar Atualizações",
            font=("Arial", 12),
            fg_color=self.accent_color,
            hover_color=self.accent_hover,
            corner_radius=8,
            height=45,
            command=check_for_updates
        )
        check_updates_button.pack(fill=tk.X, pady=(0, 5), padx=5)
        
        # Função para abrir a pasta do aplicativo
        def open_app_folder():
            try:
                os.startfile(os.getcwd())
            except:
                import subprocess
                try:
                    subprocess.Popen(f'explorer "{os.getcwd()}"')
                except:
                    pass
        
        # Botão para abrir a pasta do aplicativo
        open_folder_button = ctk.CTkButton(
            content_frame,
            text="Navegar nos arquivos do TwitchMiner",
            font=("Arial", 12),
            fg_color=self.neutral_color,
            hover_color=self.neutral_hover,
            text_color=("black", "white"),
            corner_radius=8,
            height=45,
            command=open_app_folder
        )
        open_folder_button.pack(fill=tk.X, pady=(0, 0), padx=5)
        
        return frame

    def show_tab(self, tab_name):
        """Alterna entre as abas do console e dos streams."""
        # Esconde todas as abas primeiro
        self.console_frame.pack_forget()
        self.streams_frame.pack_forget()
        self.user_frame.pack_forget()
        self.account_frame.pack_forget()
        self.about_frame.pack_forget()
        self.settings_frame.pack_forget()
        
        # Mostra a aba selecionada
        if tab_name == "console":
            self.console_frame.pack(fill=tk.BOTH, expand=True)
        elif tab_name == "streams":
            self.streams_frame.pack(fill=tk.BOTH, expand=True)
        elif tab_name == "user":
            self.user_frame.pack(fill=tk.BOTH, expand=True)
        elif tab_name == "account":
            self.account_frame.pack(fill=tk.BOTH, expand=True)
        elif tab_name == "about":
            self.about_frame.pack(fill=tk.BOTH, expand=True)
        elif tab_name == "settings":
            self.settings_frame.pack(fill=tk.BOTH, expand=True)

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

    def open_streamelements_store(self, listbox):
        """Abre a loja StreamElements do streamer selecionado."""
        try:
            # Verifica se há um streamer selecionado
            selected_index = listbox.curselection()[0]
            selected_item = listbox.get(selected_index)
            
            # Remove a numeração para obter apenas o nome do streamer
            streamer_name = selected_item.split(". ", 1)[1]
            
            # Constrói a URL da loja StreamElements
            store_url = f"https://streamelements.com/{streamer_name}/store"
            
            # Abre a URL no navegador padrão
            import webbrowser
            webbrowser.open(store_url)
            
        except IndexError:
            tk.messagebox.showwarning("Aviso", "Por favor, selecione um streamer da lista para ver sua loja StreamElements.")

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

    def update_listbox_colors(self):
        """Atualiza as cores da listbox de streams conforme o tema atual"""
        try:
            # Verifica se a listbox foi criada
            if hasattr(self, 'streams_listbox'):
                # Define cores apropriadas baseadas no tema atual
                if ctk.get_appearance_mode().lower() == "dark":
                    self.streams_listbox.config(
                        bg="#212121",
                        fg="white",
                        selectbackground="#9147ff"
                    )
                else:
                    self.streams_listbox.config(
                        bg="#f0f0f0",
                        fg="black",
                        selectbackground="#9147ff"
                    )
        except:
            pass

if __name__ == "__main__":
    app = ConsoleApp()
    app.update_console()
    app.mainloop()
