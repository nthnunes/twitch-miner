import websocket
import json
from kickapi import KickAPI

class KickChat:
    def __init__(self, channel_name="littylinhh"):
        self.ws = None
        self.is_connected = False
        self.channel_name = channel_name  # Nome do canal
        self.session_token = "235955519%7CYL4hS6XloKZ5dFuuqV4m7gNDMYrJIEw3DASgtcMi"  # Token fornecido
        self.channel_id = None
        self.chatroom_id = None
        
    def get_channel_info(self):
        """Obtém o ID do canal e do chatroom diretamente via API"""
        try:
            print(f"[INFO] Obtendo informações do canal: {self.channel_name}")
            
            import cloudscraper
            import ua_generator
            
            # Cria uma sessão com CloudScraper para contornar proteções anti-bot
            scraper = cloudscraper.create_scraper()
            ua = ua_generator.generate()
            
            # Cabeçalhos para simular um navegador real
            headers = {
                "Accept": "application/json",
                "Alt-Used": "kick.com",
                "Priority": "u=0, i",
                "Connection": "keep-alive",
                "User-Agent": ua.text,
                "Referer": f"https://kick.com/{self.channel_name}",
                "Origin": "https://kick.com"
            }
            
            # Usa o endpoint v2 da API
            url = f"https://kick.com/api/v2/channels/{self.channel_name}/chatroom"
            print(f"[INFO] Fazendo requisição para: {url}")
            
            response = scraper.get(url, headers=headers)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"[DEBUG] Resposta da API: {data}")
                    
                    self.chatroom_id = data.get("id")
                    self.channel_id = data.get("channel_id")
                    
                    print(f"[INFO] Channel ID: {self.channel_id}")
                    print(f"[INFO] Chatroom ID: {self.chatroom_id}")
                    return True
                except ValueError as e:
                    print(f"[ERRO] Falha ao processar JSON: {e}")
                    print(f"[DEBUG] Conteúdo da resposta: {response.text[:200]}...")
                    return False
            else:
                print(f"[ERRO] Falha na requisição: {response.status_code} - {response.text[:200]}...")
                return False
        except Exception as e:
            print(f"[ERRO] Exceção ao obter informações do canal: {e}")
            return False
    
    def connect(self):
        """Conecta ao chat da Kick"""
        try:
            # Primeiro obtém o ID do canal
            if not self.get_channel_info():
                print("[ERRO] Não foi possível obter o ID do canal. Encerrando o script.")
                return
                
            print(f"[INFO] Conectando ao chat da Kick no canal: {self.channel_name} (ID: {self.channel_id})")
            
            # URL do WebSocket da Kick (baseado em pesquisas)
            # A Kick usa o serviço Pusher para WebSockets
            ws_url = f"wss://ws-us2.pusher.com/app/32cbd69e4b950bf97679?protocol=7&client=js&version=8.4.0&flash=false"
            
            # Conecta ao WebSocket
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_close=self.on_close,
                on_error=self.on_error
            )
            
            # Inicia a conexão em thread principal
            self.ws.run_forever()

        except Exception as e:
            print(f"[ERRO] Falha ao conectar no chat da Kick: {e}")

    def on_open(self, ws):
        """Callback quando a conexão é estabelecida"""
        print("[INFO] Conectado ao serviço WebSocket da Kick")
        self.is_connected = True
        
        # Autentica e inscreve no canal de chat
        try:
            # Inscreve no canal de chat usando o ID do chatroom obtido
            chat_events_channel = f"chatrooms.{self.chatroom_id}.v2"
            subscribe_chat_data = {
                "event": "pusher:subscribe",
                "data": {
                    "auth": "",
                    "channel": chat_events_channel
                }
            }
            
            print(f"[DEBUG] Inscrevendo no canal de chat: {chat_events_channel}")
            self.ws.send(json.dumps(subscribe_chat_data))
            
            print("[INFO] Inscrição no canal concluída")
            
        except Exception as e:
            print(f"[ERRO] Falha na autenticação: {e}")

    def on_message(self, ws, message):
        """Callback quando recebe uma mensagem"""
        try:
            print(f"[DEBUG] Mensagem recebida: {message}")
            
            # Tenta converter a mensagem para JSON
            data = json.loads(message)
            
            # Verifica se é uma mensagem do chat
            if data.get("event") == "App\\Events\\ChatMessageEvent":
                self.parse_chat_message(data)
                
            # Responde a pings para manter a conexão viva
            if data.get("event") == "pusher:ping":
                pong_data = {"event": "pusher:pong", "data": {}}
                self.ws.send(json.dumps(pong_data))
                print("[DEBUG] Ping recebido, enviando pong")
                
        except json.JSONDecodeError:
            print(f"[ERRO] Não foi possível decodificar a mensagem: {message}")
        except Exception as e:
            print(f"[ERRO] Erro ao processar mensagem: {e}")

    def on_close(self, ws, close_status_code, close_msg):
        """Callback quando a conexão é fechada"""
        print(f"[INFO] Desconectado do chat da Kick: {close_status_code} - {close_msg}")
        self.is_connected = False

    def on_error(self, ws, error):
        """Callback quando ocorre um erro"""
        print(f"[ERRO] Erro no chat da Kick: {error}")
        self.is_connected = False

    def parse_chat_message(self, data):
        """Extrai e imprime mensagens do chat"""
        try:
            # Baseado na captura de tela, o formato correto das mensagens é:
            # {"event":"App\\Events\\ChatMessageEvent","data":"...","channel":"chatrooms.209106.v2"}
            
            # Extrai os dados da mensagem do formato JSON da Kick
            if isinstance(data, dict) and "data" in data and "event" in data:
                # Verifica se é um evento de chat
                if "ChatMessageEvent" in data["event"]:
                    try:
                        # A mensagem está em formato string JSON dentro do campo "data"
                        message_data = json.loads(data["data"])
                        
                        # Imprime os dados para debug
                        print(f"[DEBUG] Dados da mensagem: {message_data}")
                        
                        # Extrai o conteúdo da mensagem
                        if "content" in message_data:
                            content = message_data["content"]
                            
                            # Extrai o nome de usuário
                            username = "Desconhecido"
                            if "sender" in message_data and "username" in message_data["sender"]:
                                username = message_data["sender"]["username"]
                            
                            # Imprime a mensagem formatada
                            print(f"[Kick] {username}: {content}")
                        else:
                            print(f"[DEBUG] Formato de mensagem sem conteúdo: {message_data}")
                    except json.JSONDecodeError:
                        print(f"[ERRO] Não foi possível decodificar os dados da mensagem: {data['data']}")
                    except Exception as e:
                        print(f"[ERRO] Erro ao processar dados da mensagem: {e}")
            else:
                print(f"[DEBUG] Formato de mensagem não reconhecido: {data}")
        except Exception as e:
            print(f"[ERRO] Erro ao processar mensagem do chat: {e}")

    def disconnect(self):
        """Desconecta do chat"""
        if self.ws:
            self.ws.close()
            self.ws = None
        self.is_connected = False

    def get_connected(self):
        """Retorna se está conectado"""
        return self.is_connected


# Execução principal
if __name__ == "__main__":
    chat = KickChat()
    
    try:
        print("Iniciando conexão com o chat da Kick...")
        chat.connect()
    except KeyboardInterrupt:
        print("\nDesconectando...")
        chat.disconnect()
