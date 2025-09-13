import websocket
import json

class KickChat:
    def __init__(self):
        self.ws = None
        self.is_connected = False
        self.channel_name = "iamra"  # Canal padrão
        self.session_token = "235955519%7CYL4hS6XloKZ5dFuuqV4m7gNDMYrJIEw3DASgtcMi"  # Token fornecido
        
    def connect(self):
        """Conecta ao chat da Kick"""
        try:
            print(f"[INFO] Conectando ao chat da Kick no canal: {self.channel_name}")
            
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
            # Formato do canal no Pusher: channel-username
            channel_id = f"channel-{self.channel_name}"
            
            # Inscreve no canal de chat
            subscribe_data = {
                "event": "pusher:subscribe",
                "data": {
                    "auth": "",
                    "channel": channel_id
                }
            }
            
            print(f"[DEBUG] Inscrevendo no canal: {channel_id}")
            self.ws.send(json.dumps(subscribe_data))
            
            # Inscreve no canal de chat-events que contém mensagens
            # Vendo sua captura de tela, o formato correto é chatrooms.209106.v2
            # Vamos tentar obter o ID do chatroom a partir do nome do canal
            
            # Primeiro tenta com o ID do canal que você está vendo (209106)
            chat_events_channel = f"chatrooms.3925550.v2"
            subscribe_chat_data = {
                "event": "pusher:subscribe",
                "data": {
                    "auth": "",
                    "channel": chat_events_channel
                }
            }
            
            print(f"[DEBUG] Inscrevendo no canal de chat específico: {chat_events_channel}")
            self.ws.send(json.dumps(subscribe_chat_data))
            
            # Também tenta com o nome do canal (pode ser necessário para outros canais)
            chat_events_channel2 = f"chatrooms.{self.channel_name}.v2"
            subscribe_chat_data2 = {
                "event": "pusher:subscribe",
                "data": {
                    "auth": "",
                    "channel": chat_events_channel2
                }
            }
            
            print(f"[DEBUG] Inscrevendo no canal de chat com nome: {chat_events_channel2}")
            self.ws.send(json.dumps(subscribe_chat_data2))
            
            print("[INFO] Inscrição nos canais concluída")
            
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
