import os, sys
import inquirer
import pythoncom
from win32comext.shell import shell, shellcon
import ctypes.wintypes
import time


def createShortcut():
    if not os.path.exists("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\TwitchMinerSecond.lnk"):
        shortcut = pythoncom.CoCreateInstance (
        shell.CLSID_ShellLink,
        None,
        pythoncom.CLSCTX_INPROC_SERVER,
        shell.IID_IShellLink
        )
        shortcut.SetPath (sys.executable)
        shortcut.SetDescription ("Python %s" % sys.version)
        shortcut.SetIconLocation (sys.executable, 0)

        persist_file = shortcut.QueryInterface (pythoncom.IID_IPersistFile)
        persist_file.Save("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\TwitchMinerSecond.lnk", 0)
    
    if not os.path.exists("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\TwitchMinerSecond.lnk"):
        shortcut = pythoncom.CoCreateInstance (
        shell.CLSID_ShellLink,
        None,
        pythoncom.CLSCTX_INPROC_SERVER,
        shell.IID_IShellLink
        )
        shortcut.SetPath (sys.executable)
        shortcut.SetDescription ("Python %s" % sys.version)
        shortcut.SetIconLocation (sys.executable, 0)

        persist_file = shortcut.QueryInterface (pythoncom.IID_IPersistFile)
        persist_file.Save("C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\TwitchMinerSecond.lnk", 0)


def scanStreamers():
    if not os.path.exists('./streamers.txt'):
        time.sleep(1)
        num_streamers = int(input("Number of streamers to watch: "))
        streamers = []

        for i in range(1, num_streamers + 1):
            username = input(f"{i}. Streamer Username: ")
            streamers.append(username)

        with open("streamers.txt", "w") as data:
            for streamer in streamers:
                data.write(streamer + "\n")

        return streamers
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
    final_path = formatted_path + "\\\\TwitchMinerSecond"
    os.chdir(final_path)
    
    if not os.path.exists('./username.txt'):
        username = input("Your Twitch Username: ")
        data = open("username.txt", "w")
        data.write(username)
        data.close()
        createShortcut()
        return username
    else:
        data = open("username.txt", "r")
        username = data.readline()
        data.close()
        return username