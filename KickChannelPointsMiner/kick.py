import websocket
import json
import cloudscraper
import ua_generator

class KickChat:
    def __init__(self, channel_name, session_token, DEBUG=False):
        self.ws = None
        self.is_connected = False
        self.channel_name = channel_name
        self.session_token = session_token
        self.chatroom_id = None
        self.DEBUG = DEBUG
        
    def get_channel_info(self):
        """Get chatroom ID from Kick API"""
        try:
            print(f"[INFO] Obtendo informações do canal: {self.channel_name}")
            
            scraper = cloudscraper.create_scraper()
            ua = ua_generator.generate()
            
            headers = {
                "Accept": "application/json",
                "Alt-Used": "kick.com",
                "Priority": "u=0, i",
                "Connection": "keep-alive",
                "User-Agent": ua.text,
                "Referer": f"https://kick.com/{self.channel_name}",
                "Origin": "https://kick.com"
            }
            
            url = f"https://kick.com/api/v2/channels/{self.channel_name}/chatroom"
            if self.DEBUG:
                print(f"[DEBUG] Fazendo requisição para: {url}")
            
            response = scraper.get(url, headers=headers)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if self.DEBUG:
                        print(f"[DEBUG] Resposta da API: {data}")
                    
                    self.chatroom_id = data.get("id")
                    print(f"[INFO] Chatroom ID: {self.chatroom_id}")
                    return True
                except ValueError as e:
                    print(f"[ERRO] Falha ao processar JSON: {e}")
                    if self.DEBUG:
                        print(f"[DEBUG] Conteúdo da resposta: {response.text[:200]}...")
                    return False
            else:
                print(f"[ERRO] Falha na requisição: {response.status_code} - {response.text[:200]}...")
                return False
        except Exception as e:
            print(f"[ERRO] Exceção ao obter informações do canal: {e}")
            return False
    
    def connect(self):
        """Connect to Kick chat"""
        try:
            if not self.get_channel_info():
                print("[ERRO] Não foi possível obter o ID do chatroom. Encerrando.")
                return
                
            print(f"[INFO] Conectando ao chat da Kick: {self.channel_name} (ID: {self.chatroom_id})")
            
            ws_url = f"wss://ws-us2.pusher.com/app/32cbd69e4b950bf97679?protocol=7&client=js&version=8.4.0&flash=false"
            
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_close=self.on_close,
                on_error=self.on_error
            )
            
            self.ws.run_forever()

        except Exception as e:
            print(f"[ERRO] Falha ao conectar no chat da Kick: {e}")

    def on_open(self, ws):
        """WebSocket connection established"""
        print("[INFO] Conectado ao WebSocket da Kick")
        self.is_connected = True
        
        try:
            chat_events_channel = f"chatrooms.{self.chatroom_id}.v2"
            subscribe_chat_data = {
                "event": "pusher:subscribe",
                "data": {
                    "auth": "",
                    "channel": chat_events_channel
                }
            }
            
            if self.DEBUG:
                print(f"[DEBUG] Inscrevendo no canal de chat: {chat_events_channel}")
            self.ws.send(json.dumps(subscribe_chat_data))
            
            print("[INFO] Inscrição no canal concluída")
            
        except Exception as e:
            print(f"[ERRO] Falha na autenticação: {e}")

    def on_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        try:
            if self.DEBUG:
                print(f"[DEBUG] Mensagem recebida: {message}")
            
            data = json.loads(message)
            
            if data.get("event") == "App\\Events\\ChatMessageEvent":
                self.parse_chat_message(data)
                
            if data.get("event") == "pusher:ping":
                pong_data = {"event": "pusher:pong", "data": {}}
                self.ws.send(json.dumps(pong_data))
                if self.DEBUG:
                    print("[DEBUG] Ping recebido, enviando pong")
                
        except json.JSONDecodeError:
            print(f"[ERRO] Não foi possível decodificar a mensagem: {message}")
        except Exception as e:
            print(f"[ERRO] Erro ao processar mensagem: {e}")

    def on_close(self, ws, close_status_code, close_msg):
        """WebSocket connection closed"""
        print(f"[INFO] Desconectado do chat da Kick: {close_status_code} - {close_msg}")
        self.is_connected = False

    def on_error(self, ws, error):
        """WebSocket error occurred"""
        print(f"[ERRO] Erro no chat da Kick: {error}")
        self.is_connected = False

    def parse_chat_message(self, data):
        """Parse and print chat messages"""
        try:
            if isinstance(data, dict) and "data" in data and "event" in data:
                if "ChatMessageEvent" in data["event"]:
                    try:
                        message_data = json.loads(data["data"])
                        
                        if self.DEBUG:
                            print(f"[DEBUG] Dados da mensagem: {message_data}")
                        
                        if "content" in message_data:
                            content = message_data["content"]
                            username = "Desconhecido"
                            if "sender" in message_data and "username" in message_data["sender"]:
                                username = message_data["sender"]["username"]
                            
                            print(f"[Kick] {username}: {content}")
                        else:
                            if self.DEBUG:
                                print(f"[DEBUG] Mensagem sem conteúdo: {message_data}")
                    except json.JSONDecodeError:
                        print(f"[ERRO] Não foi possível decodificar os dados da mensagem: {data['data']}")
                    except Exception as e:
                        print(f"[ERRO] Erro ao processar dados da mensagem: {e}")
            else:
                if self.DEBUG:
                    print(f"[DEBUG] Formato de mensagem não reconhecido: {data}")
        except Exception as e:
            print(f"[ERRO] Erro ao processar mensagem do chat: {e}")

    def disconnect(self):
        """Disconnect from chat"""
        if self.ws:
            self.ws.close()
            self.ws = None
        self.is_connected = False

    def get_connected(self):
        """Check if connected"""
        return self.is_connected


if __name__ == "__main__":
    chat = KickChat("theleaway", "", DEBUG=True)
    
    try:
        print("Iniciando conexão com o chat da Kick...")
        chat.connect()
    except KeyboardInterrupt:
        print("\nDesconectando...")
        chat.disconnect()
