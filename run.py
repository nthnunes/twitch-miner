# -*- coding: utf-8 -*-

import logging
from colorama import Fore
from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.logger import LoggerSettings, ColorPalette
from TwitchChannelPointsMiner.classes.Chat import ChatPresence
from TwitchChannelPointsMiner.classes.Discord import Discord
from TwitchChannelPointsMiner.classes.Webhook import Webhook
from TwitchChannelPointsMiner.classes.Telegram import Telegram
from TwitchChannelPointsMiner.classes.Matrix import Matrix
from TwitchChannelPointsMiner.classes.Pushover import Pushover
from TwitchChannelPointsMiner.classes.Settings import Priority, Events, FollowersOrder
from TwitchChannelPointsMiner.classes.entities.Bet import Strategy, BetSettings, Condition, OutcomeKeys, FilterCondition, DelayMode
from TwitchChannelPointsMiner.classes.entities.Streamer import Streamer, StreamerSettings
import os
import time
import logging
import threading
import webbrowser
from scanner import scanStreamers, scanUsername, load_auto_update, save_auto_update, search_updates, connectUsername, createShortcut
import tkinter as tk
from ui import display_streamers, display_username
import pystray
from PIL import Image
import requests
from io import BytesIO
import ctypes.wintypes
import queue
from window_manager import WindowManager, show_window
import asyncio
from twitch_viewer import monitor_channel
from ads_viewer import run_loop

# Cria uma fila para comunicação entre threads
window_queue = queue.Queue()

CSIDL_PERSONAL = 5       # My Documents
SHGFP_TYPE_CURRENT = 0   # Get current, not default value
buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
original_path = buf.value
formatted_path = original_path.replace("\\", "\\\\")
final_path = formatted_path + "\\\\TwitchMiner"
os.chdir(final_path)

auto_update = load_auto_update()
version = "2.0.5"

# Flags para indicar quando abrir as janelas
open_username_window = False
open_streamers_window = False


def auto_updater():
    while True:
        if load_auto_update():
            update_thread = threading.Thread(target=search_updates, args=(load_auto_update(), version))
            update_thread.start()
            update_thread
        # Wait 24 hours (86.400 seconds)
        time.sleep(86400)

def onBackground():
    icon_url = "https://8upload.com/image/652f72aea6996/icon-windowed.png"
    response = requests.get(icon_url)
    image = Image.open(BytesIO(response.content))

    global auto_update

    def after_click(icon, query):
        global auto_update
        if str(query) == "Abrir Painel":
            show_window()
        elif str(query) == "Ver Estatísticas":
            webbrowser.open("http://localhost:5000")
        elif str(query) == "Sair":
            icon.stop()
            os._exit(0)

    icon = pystray.Icon("TM", image, "TwitchMiner v" + version, 
        menu=pystray.Menu(
            pystray.MenuItem("Abrir Painel", after_click),
            pystray.MenuItem("Ver Estatísticas", after_click),
            pystray.MenuItem("Sair", after_click)))
    return icon

def open_windows_if_needed():
    try:
        # Verifica se há alguma mensagem na fila
        while not window_queue.empty():
            message = window_queue.get_nowait()
            if message == "username":
                root2 = tk.Tk()
                display_username(root2)
            elif message == "streams":
                root2 = tk.Tk()
                display_streamers(root2)
    except queue.Empty:
        pass  # Ignora se a fila estiver vazia

def start_mining(twitch_miner):
    twitch_miner.analytics(host="localhost", port=5000, refresh=5, days_ago=7)
    
    streamers = scanStreamers() or []

    streamers_list = [Streamer("nthnunes")] + [Streamer(s) for s in streamers if s]
    twitch_miner.mine(
        streamers_list,                         # Array dinâmico de streamers (ordem = prioridade)
        followers=False,                        # Não baixa automaticamente a lista de seguidores
        followers_order=FollowersOrder.ASC      # Ordena a lista de seguidores por data de follow. ASC ou DESC
    )

if __name__ == "__main__":
    if not os.path.exists('./username.txt'):
        connectUsername()
        createShortcut()

    # Inicializa o ícone da bandeja
    icon = onBackground()

    # Inicializa o gerenciador da janela com o ícone da bandeja
    WindowManager.get_instance().initialize(icon)

    # Obtém a instância do ConsoleApp
    app = WindowManager.get_instance().app

    # Inicializa o twitch_viewer em uma thread separada
    def run_twitch_viewer():
        asyncio.run(monitor_channel())

    # Inicializa o ads_viewer em uma thread separada
    def run_ads_viewer():
        asyncio.run(run_loop())

    twitch_miner = TwitchChannelPointsMiner(
        username=scanUsername(),
        password="",                                # If no password will be provided, the script will ask interactively
        claim_drops_startup=False,                  # If you want to auto claim all drops from Twitch inventory on the startup
        priority=[                                  # Custom priority in this case for example:
            Priority.STREAK,                        # - We want first of all to catch all watch streak from all streamers
            Priority.DROPS,                         # - When we don't have anymore watch streak to catch, wait until all drops are collected over the streamers
            Priority.ORDER                          # - When we have all of the drops claimed and no watch-streak available, use the order priority (POINTS_ASCENDING, POINTS_DESCENDING)
        ],
        enable_analytics=True,                     # Disables Analytics if False. Disabling it significantly reduces memory consumption
        disable_ssl_cert_verification=False,        # Set to True at your own risk and only to fix SSL: CERTIFICATE_VERIFY_FAILED error
        disable_at_in_nickname=False,               # Set to True if you want to check for your nickname mentions in the chat even without @ sign
        logger_settings=LoggerSettings(
            save=True,                              # If you want to save logs in a file (suggested)
            console_level=logging.INFO,             # Level of logs - use logging.DEBUG for more info
            console_username=False,                 # Adds a username to every console log line if True. Also adds it to Telegram, Discord, etc. Useful when you have several accounts
            auto_clear=True,                        # Create a file rotation handler with interval = 1D and backupCount = 7 if True (default)
            time_zone="America/Sao_Paulo",          # Set a specific time zone for console and file loggers. Use tz database names. Example: "America/Denver"
            file_level=logging.DEBUG,               # Level of logs - If you think the log file it's too big, use logging.INFO
            emoji=True,                             # On Windows, we have a problem printing emoji. Set to false if you have a problem
            less=False,                             # If you think that the logs are too verbose, set this to True
            colored=True,                           # If you want to print colored text
            color_palette=ColorPalette(             # You can also create a custom palette color (for the common message).
                STREAMER_online="GREEN",            # Don't worry about lower/upper case. The script will parse all the values.
                streamer_offline="red",             # Read more in README.md
                BET_wiN=Fore.MAGENTA                # Color allowed are: [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET].
            ),
            telegram=Telegram(                                                          # You can omit or set to None if you don't want to receive updates on Telegram
                chat_id=123456789,                                                      # Chat ID to send messages @getmyid_bot
                token="123456789:shfuihreuifheuifhiu34578347",                          # Telegram API token @BotFather
                events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE,
                        Events.BET_LOSE, Events.CHAT_MENTION],                          # Only these events will be sent to the chat
                disable_notification=True,                                              # Revoke the notification (sound/vibration)
            ),
            discord=Discord(
                webhook_api="https://discord.com/api/webhooks/0123456789/0a1B2c3D4e5F6g7H8i9J",  # Discord Webhook URL
                events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE,
                        Events.BET_LOSE, Events.CHAT_MENTION],                                  # Only these events will be sent to the chat
            ),
            webhook=Webhook(
                endpoint="https://example.com/webhook",                                                                    # Webhook URL
                method="GET",                                                                   # GET or POST
                events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE,
                        Events.BET_LOSE, Events.CHAT_MENTION],                                  # Only these events will be sent to the endpoint
            ),
            matrix=Matrix(
                username="twitch_miner",                                                   # Matrix username (without homeserver)
                password="...",                                                            # Matrix password
                homeserver="matrix.org",                                                   # Matrix homeserver
                room_id="...",                                                             # Room ID
                events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE, Events.BET_LOSE], # Only these events will be sent
            ),
            pushover=Pushover(
                userkey="YOUR-ACCOUNT-TOKEN",                                             # Login to https://pushover.net/, the user token is on the main page
                token="YOUR-APPLICATION-TOKEN",                                           # Create a application on the website, and use the token shown in your application
                priority=0,                                                               # Read more about priority here: https://pushover.net/api#priority
                sound="pushover",                                                         # A list of sounds can be found here: https://pushover.net/api#sounds
                events=[Events.CHAT_MENTION, Events.DROP_CLAIM],                          # Only these events will be sent
            )
        ),
        streamer_settings=StreamerSettings(
            make_predictions=False,                  # If you want to Bet / Make prediction
            follow_raid=False,                       # Follow raid to obtain more points
            claim_drops=True,                       # We can't filter rewards base on stream. Set to False for skip viewing counter increase and you will never obtain a drop reward from this script. Issue #21
            claim_moments=True,                     # If set to True, https://help.twitch.tv/s/article/moments will be claimed when available
            watch_streak=True,                      # If a streamer go online change the priority of streamers array and catch the watch screak. Issue #11
            chat=ChatPresence.ONLINE,               # Join irc chat to increase watch-time [ALWAYS, NEVER, ONLINE, OFFLINE]
            bet=BetSettings(
                strategy=Strategy.SMART,            # Choose you strategy!
                percentage=5,                       # Place the x% of your channel points
                percentage_gap=20,                  # Gap difference between outcomesA and outcomesB (for SMART strategy)
                max_points=50000,                   # If the x percentage of your channel points is gt bet_max_points set this value
                stealth_mode=True,                  # If the calculated amount of channel points is GT the highest bet, place the highest value minus 1-2 points Issue #33
                delay_mode=DelayMode.FROM_END,      # When placing a bet, we will wait until `delay` seconds before the end of the timer
                delay=6,
                minimum_points=20000,               # Place the bet only if we have at least 20k points. Issue #113
                filter_condition=FilterCondition(
                    by=OutcomeKeys.TOTAL_USERS,     # Where apply the filter. Allowed [PERCENTAGE_USERS, ODDS_PERCENTAGE, ODDS, TOP_POINTS, TOTAL_USERS, TOTAL_POINTS]
                    where=Condition.LTE,            # 'by' must be [GT, LT, GTE, LTE] than value
                    value=800
                )
            )
        )
    )

    # Executa o ícone da bandeja em uma thread separada
    tray_thread = threading.Thread(target=icon.run, daemon=True)
    tray_thread.start()

    # Inicializa o minerador em uma thread separada
    mining_thread = threading.Thread(target=start_mining, args=(twitch_miner,), daemon=True)
    mining_thread.start()

    # Inicializa o auto-updater em uma thread separada
    auto_updater_thread = threading.Thread(target=auto_updater, daemon=True)
    auto_updater_thread.start()

    # Inicializa o twitch_viewer em uma thread separada
    twitch_viewer_thread = threading.Thread(target=run_twitch_viewer, daemon=True)
    twitch_viewer_thread.start()

    # Inicializa o ads_viewer em uma thread separada
    ads_viewer_thread = threading.Thread(target=run_ads_viewer, daemon=True)
    ads_viewer_thread.start()

    # Atualiza o console periodicamente
    app.update_console()
    app.mainloop()

    # Loop principal para abrir as janelas quando sinalizado
    while True:
        open_windows_if_needed()
        time.sleep(0.1)  # Pequena pausa para evitar uso excessivo da CPU