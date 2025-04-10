import logging
import time
from enum import Enum, auto
from threading import Thread
import scanner
from win10toast import ToastNotifier
from irc.bot import SingleServerIRCBot

from TwitchChannelPointsMiner.constants import IRC, IRC_PORT
from TwitchChannelPointsMiner.classes.Settings import Events, Settings

toaster = ToastNotifier()

logger = logging.getLogger(__name__)

class ChatPresence(Enum):
    ALWAYS = auto()
    NEVER = auto()
    ONLINE = auto()
    OFFLINE = auto()

    def __str__(self):
        return self.name


class ClientIRC(SingleServerIRCBot):
    def __init__(self, username, token, channel, notification_toaster=None):
        self.token = token
        self.channel = "#" + channel
        self.__active = False
        self.notification_toaster = notification_toaster if notification_toaster else toaster

        super(ClientIRC, self).__init__(
            [(IRC, IRC_PORT, f"oauth:{token}")], username, username
        )

    def on_welcome(self, client, event):
        client.join(self.channel)

    def start(self):
        self.__active = True
        self._connect()
        while self.__active:
            try:
                self.reactor.process_once(timeout=0.2)
                time.sleep(0.01)
            except Exception as e:
                logger.error(
                    f"Exception raised: {e}. Thread is active: {self.__active}"
                )

    def die(self, msg="Bye, cruel world!"):
        self.connection.disconnect(msg)
        self.__active = False

    """
    def on_join(self, connection, event):
        logger.info(f"Event: {event}", extra={"emoji": ":speech_balloon:"})
    """

    def on_pubmsg(self, connection, event):
        msg = event.arguments[0]
        mention = None

        if Settings.disable_at_in_nickname is True:
            mention = f"{self._nickname.lower()}"
        else:
            mention = f"@{self._nickname.lower()}"

        # also self._realname
        # if msg.startswith(f"@{self._nickname}"):
        if mention != None and mention in msg.lower():
            # nickname!username@nickname.tmi.twitch.tv
            nick = event.source.split("!", 1)[0]
            # chan = event.target

            logger.info(f"{nick} em {self.channel} escreveu: {msg}", extra={
                        "emoji": ":speech_balloon:", "event": Events.CHAT_MENTION})
            
            # Verifica se as notificações de chat estão habilitadas antes de exibir
            chat_notifications_enabled = True
            try:
                # Carrega a configuração de notificações do chat do scanner
                chat_notifications_enabled = scanner.load_chat_notifications()
            except Exception as e:
                logger.error(f"Erro ao verificar configuração de notificações: {e}")
                pass
            
            if chat_notifications_enabled and self.notification_toaster:
                try:
                    channel_name = self.channel.replace("#", "")
                    self.notification_toaster.show_toast(
                        f"Menção no Chat da Twitch - {channel_name}",
                        f"{nick}: {msg}",
                        duration=5,
                        threaded=True
                    )
                except Exception as e:
                    logger.error(f"Erro ao mostrar notificação: {e}")


class ThreadChat(Thread):
    def __deepcopy__(self, memo):
        return None

    def __init__(self, username, token, channel, notification_toaster=None):
        super(ThreadChat, self).__init__()

        self.username = username
        self.token = token
        self.channel = channel
        self.notification_toaster = notification_toaster if notification_toaster else toaster

        self.chat_irc = None

    def run(self):
        # Passa o objeto toaster recebido pelo ThreadChat para ClientIRC
        self.chat_irc = ClientIRC(self.username, self.token, self.channel, self.notification_toaster)
        logger.info(
            f"Chat conectado: {self.channel}", extra={"emoji": ":speech_balloon:"}
        )
        
        # Verifica se as notificações de chat conectado estão habilitadas antes de exibir
        chat_connected_notifications_enabled = True
        try:
            # Carrega a configuração de notificações de chat conectado do scanner
            chat_connected_notifications_enabled = scanner.load_chat_connected_notifications()
        except Exception as e:
            logger.error(f"Erro ao verificar configuração de notificações de chat conectado: {e}")
            pass
        
        if chat_connected_notifications_enabled and self.notification_toaster:
            try:
                channel_name = self.channel.replace("#", "")
                self.notification_toaster.show_toast(
                    f"@{channel_name} está online!",
                    f"Conectado com sucesso ao chat da twitch",
                    duration=3,
                    threaded=True
                )
            except Exception as e:
                logger.error(f"Erro ao mostrar notificação de chat conectado: {e}")
        
        self.chat_irc.start()

    def stop(self):
        if self.chat_irc is not None:
            logger.info(
                f"Chat desconectado: {self.channel}", extra={"emoji": ":speech_balloon:"}
            )
            self.chat_irc.die()
