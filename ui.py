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



# Function to load usernames from the file
def load_usernames():
    try:
        with open("usernames.txt", "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        return []

# Function to save usernames to the file
def save_usernames(usernames):
    with open("usernames.txt", "w") as file:
        for username in usernames:
            file.write(f"{username}\n")

# Function to refresh usernames listbox
def refresh_username_listbox():
    username_listbox.delete(0, END)
    usernames = load_usernames()
    for index, username in enumerate(usernames, start=1):
        username_listbox.insert(END, f"{username}")

# Function to add a new username
def add_username():
    new_username = username_entry.get().strip()
    if new_username:
        username_listbox.insert(END, f"{new_username}")
        username_entry.delete(0, END)
        save_usernames(username_listbox.get(0, END))
    else:
        messagebox.showwarning("Erro", "O nome de usuário não pode estar vazio.")

# Function to remove the selected username
def remove_username():
    try:
        selected_index = username_listbox.curselection()[0]
        username_listbox.delete(selected_index)
        save_usernames(username_listbox.get(0, END))
        refresh_username_listbox()
    except IndexError:
        messagebox.showwarning("Erro", "Selecione uma conta para removê-la.")

# Function to save accounts and close
def change_username(root):
    # This is slightly misleading name now as it saves multiple, but kept for compatibility
    save_usernames(username_listbox.get(0, END))
    messagebox.showinfo("Alteração de Conta", "Contas alteradas! Para as alterações surtirem efeito reinicie o bot.")
    root.destroy()

# Função principal para exibir a interface
def display_username(root):
    global username_entry, username_listbox
    root.title("Alterar Contas Twitch")

    # Definindo o tamanho da janela
    window_width = 450
    window_height = 350

    # Calculando a posição para centralizar a janela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    main_frame = Frame(root)
    main_frame.pack(padx=10, pady=10)

    # Label for the title
    title_label = Label(main_frame, text="Contas Twitch conectadas:", font=("Arial", 12, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

    # Creating the Listbox to display usernames
    username_listbox = Listbox(main_frame, width=30, height=10)
    username_listbox.grid(row=1, column=0, rowspan=4, padx=(0, 10), pady=5)

    # Populating the listbox initially
    refresh_username_listbox()

    # Entry field to add a new username
    username_entry = Entry(main_frame, width=25)
    username_entry.grid(row=1, column=1, pady=(5, 0), sticky="w")

    # Button to add a new username
    add_button = Button(main_frame, text="Adicionar Conta", command=add_username)
    add_button.grid(row=2, column=1, pady=(5, 0), sticky="ew")

    # Button to remove a selected username
    remove_button = Button(main_frame, text="Remover Conta", command=remove_username)
    remove_button.grid(row=3, column=1, pady=5, sticky="ew")

    # Button to save and restart the bot
    restart_button = Button(main_frame, text="Salvar e Sair", command=lambda: change_username(root))
    restart_button.grid(row=4, column=1, pady=5, sticky="ew")

    # Texto de observação abaixo do botão
    obs_label = Label(root, text="Observação: Ao alterar suas contas, o bot precisará ser reiniciado, e você fará o login no terminal.", font=("Arial", 8), wraplength=400, justify="center")
    obs_label.pack(pady=(5, 10), padx=20)

    root.mainloop()
