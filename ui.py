from tkinter import Listbox, Entry, Button, END, messagebox, Frame, Label

# Function to read streamers from the file
def read_streamers():
    try:
        with open("streamers.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return ["File 'streamers.txt' not found."]

# Function to save streamers to the file
def save_streamers(streamers):
    with open("streamers.txt", "w") as file:
        for streamer in streamers:
            file.write(f"{streamer}\n")

# Function to refresh listbox with numbers
def refresh_listbox():
    listbox.delete(0, END)
    streamers = read_streamers()
    for index, streamer in enumerate(streamers, start=1):
        listbox.insert(END, f"{index}. {streamer}")

# Function to add a streamer
def add_streamer():
    streamer = entry.get().strip()
    if streamer:
        listbox.insert(END, f"{listbox.size() + 1}. {streamer}")
        entry.delete(0, END)
        save_streamers([listbox.get(i).split(". ", 1)[1] for i in range(listbox.size())])
    else:
        messagebox.showwarning("Erro", "Insira o nome de usuário de um streamer para adicioná-lo.")

# Function to remove a selected streamer
def remove_streamer():
    try:
        selected_index = listbox.curselection()[0]
        listbox.delete(selected_index)
        save_streamers([listbox.get(i).split(". ", 1)[1] for i in range(listbox.size())])
        refresh_listbox()
    except IndexError:
        messagebox.showwarning("Erro", "Selecione um streamer para removê-lo.")

# Function to handle the start of a drag
def start_drag(event):
    global drag_data
    drag_data = {"index": listbox.nearest(event.y)}

# Function to handle the dragging motion
def on_drag(event):
    nearest_index = listbox.nearest(event.y)
    if nearest_index != drag_data["index"]:
        item = listbox.get(drag_data["index"])
        listbox.delete(drag_data["index"])
        listbox.insert(nearest_index, item)
        drag_data["index"] = nearest_index
        save_streamers([listbox.get(i).split(". ", 1)[1] for i in range(listbox.size())])
        refresh_listbox()

# Function to simulate restarting the bot
def restart_bot(root):
    # Exibindo uma mensagem de confirmação
    messagebox.showinfo("Alteração bem-sucedida", f"Para as alterações surtirem efeito reinicie o bot.")
        
    # Fechando a janela principal
    root.destroy()

# Function to display the window in the center of the screen
def display_streamers(root):
    global entry, listbox, drag_data
    drag_data = {"index": 0}  # Initialize drag data

    # Creating the main window
    root.title("Lista de Streamers")

    # Defining the size of the window
    window_width = 500
    window_height = 330

    # Calculating the position to center the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Creating a frame for horizontal layout
    main_frame = Frame(root)
    main_frame.pack(padx=10, pady=10)

    # Label for the title
    title_label = Label(main_frame, text="Ordem de prioridade:", font=("Arial", 12, "bold"))
    title_label.grid(row=0, column=0, columnspan=3, pady=(0, 1), sticky="w")

    # Subtext label for drag-and-drop instruction
    instruction_label = Label(main_frame, text="Segure e arraste para alterar as posições da lista.", font=("Arial", 8))
    instruction_label.grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky="w")

    # Creating the Listbox to display streamers
    listbox = Listbox(main_frame, width=40, height=15)
    listbox.grid(row=2, column=0, rowspan=6, padx=(0, 10), pady=5)

    # Populating the listbox initially
    refresh_listbox()

    # Label for twitch.tv prefix
    twitch_label = Label(main_frame, text="twitch.tv/", font=("Arial", 10))
    twitch_label.grid(row=2, column=1, sticky="e")

    # Entry field to add a new streamer
    entry = Entry(main_frame, width=25)
    entry.grid(row=2, column=2, pady=(5, 0), sticky="w")

    # Button to add a new streamer with full width
    add_button = Button(main_frame, text="Adicionar streamer", command=add_streamer)
    add_button.grid(row=3, column=1, columnspan=2, pady=(0, 70), sticky="ew")

    # Button to remove a selected streamer
    remove_button = Button(main_frame, text="Remover selecionado", command=remove_streamer)
    remove_button.grid(row=4, column=1, columnspan=2, pady=5, sticky="ew")

    # Button to save and restart the bot
    restart_button = Button(main_frame, text="Aplicar alterações", command=lambda: restart_bot(root))
    restart_button.grid(row=5, column=1, columnspan=2, pady=5, sticky="ew")

    # Bind mouse events for drag-and-drop
    listbox.bind("<Button-1>", start_drag)
    listbox.bind("<B1-Motion>", on_drag)

    root.mainloop()



# Função para carregar o nome de usuário do arquivo
def load_username():
    try:
        with open("username.txt", "r") as file:
            username = file.readline().strip()
        return username
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo 'username.txt' não encontrado.")
        return ""

# Função para atualizar o nome de usuário no arquivo e fechar a janela
def change_username(root):
    new_username = username_entry.get().strip()
    if new_username:
        # Salvando o novo nome de usuário no arquivo
        with open("username.txt", "w") as file:
            file.write(new_username)
        
        # Exibindo uma mensagem de confirmação
        messagebox.showinfo("Alteração de Conta", f"Conta alterada para: {new_username}\n\nPara as alterações surtirem efeito reinicie o bot.")
        
        # Fechando a janela principal
        root.destroy()
    else:
        messagebox.showwarning("Erro", "O nome de usuário não pode estar vazio.")

# Função principal para exibir a interface
def display_username(root):
    global username_entry
    root.title("Alterar Conta Twitch")

    # Definindo o tamanho da janela
    window_width = 400
    window_height = 180

    # Calculando a posição para centralizar a janela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Carregando o nome de usuário do arquivo
    username = load_username()

    # Rótulo para o campo de entrada
    username_label = Label(root, text="Seu nome de usuário:")
    username_label.pack(pady=(10, 5))

    # Frame para o campo de entrada, com espaçamento lateral
    entry_frame = Frame(root)
    entry_frame.pack(padx=20)  # Espaçamento lateral

    # Campo de entrada para o nome de usuário
    username_entry = Entry(entry_frame, width=30)
    username_entry.pack(pady=5)
    username_entry.insert(0, username)  # Inserindo o nome de usuário carregado

    # Botão para alterar a conta
    change_button = Button(root, text="Alterar conta Twitch", command=lambda: change_username(root))
    change_button.pack(pady=10)

    # Texto de observação abaixo do botão
    obs_label = Label(root, text="Observação: Ao alterar seu nome de usuário na Twitch, o bot será reiniciado, e você precisará fazer login com o novo usuário.", font=("Arial", 8), wraplength=350, justify="left")
    obs_label.pack(pady=(5, 10), padx=20)

    root.mainloop()
