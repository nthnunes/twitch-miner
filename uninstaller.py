import ctypes
import ctypes.wintypes
import os
import shutil
import inquirer

CSIDL_PERSONAL = 5
SHGFP_TYPE_CURRENT = 0

buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

original_path = buf.value
formatted_path = original_path.replace("\\", "\\\\")
twitchminer_path = os.path.join(formatted_path, "TwitchMiner")
uninstaller_path = os.path.join(twitchminer_path, "desinstalar.exe")

def confirm_uninstall():
    question = [
        inquirer.List(
            "confirm",
            message="Tem certeza de que deseja desinstalar? Todos os dados do TwitchMiner serão removidos",
            choices=["Sim", "Não"],
        )
    ]
    answer = inquirer.prompt(question)
    return answer["confirm"] == "Sim"


if confirm_uninstall():
    print("Desinstalando TwitchMiner, aguarde...")

    for item in os.listdir(twitchminer_path):
        item_path = os.path.join(twitchminer_path, item)
        if item_path != uninstaller_path:
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        
    startup_shortcut_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\TwitchMiner.lnk"
    programs_shortcut_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\TwitchMiner.lnk"

    if os.path.exists(startup_shortcut_path):
        os.remove(startup_shortcut_path)
        print("-> Inicialização automática removida.")
    else:
        print("-> Inicialização automática não encontrada.")

    if os.path.exists(programs_shortcut_path):
        os.remove(programs_shortcut_path)
        print("-> Atalho removido da pasta de Programas.")
    else:
        print("-> Atalho da pasta de programas não encontrado.")

    print("-> TwitchMiner desinstalado com sucesso.")
    print("Agora apague a pasta TwitchMiner da sua pasta de Documentos e estará tudo concluído. Até a próxima!")
else:
    print("Desinstalação cancelada, saindo...")
