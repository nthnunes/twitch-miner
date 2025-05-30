import asyncio
import shutil
import aiohttp
from playwright.async_api import async_playwright
from datetime import datetime

# Nome do canal do Twitch para assistir
CHANNEL_NAME = "nthnunes"
# Intervalo de verificação em segundos (5 minutos)
CHECK_INTERVAL = 300

# Variáveis globais para controlar o estado
active_browser = None
active_page = None

# Detecta automaticamente o caminho do Google Chrome
def find_chrome_path():
    import os

    possible_paths = [
        shutil.which("google-chrome"),
        shutil.which("chrome"),
        shutil.which("chromium"),
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium"
    ]
    for path in possible_paths:
        if path and os.path.exists(path):
            return path
    return None


# Acessa a Twitch diretamente
async def watch_twitch(channel_name, playwright):
    print(f"{datetime.now().strftime('%d/%m/%y %H:%M:%S')} - INFO - [twitch_viewer]: Iniciando navegador para assistir o canal: {channel_name}")
    twitch_url = f"https://www.twitch.tv/{channel_name}"

    chrome_path = find_chrome_path()
    if not chrome_path:
        #print("Chrome não encontrado no sistema.")
        return

    browser = await playwright.chromium.launch(
        headless=True,
        executable_path=chrome_path,
        args=[
            "--disable-dev-shm-usage",
            "--disable-extensions",
            "--disable-gpu",
            "--no-sandbox"
        ]
    )

    context = await browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        timezone_id="America/New_York",
        locale="en-US"
    )

    page = await context.new_page()
    try:
        await page.goto(twitch_url, wait_until="load")
        #print("Conectado com sucesso!")

        # Mutar e forçar autoplay do vídeo
        await page.evaluate("""
            try {
                const video = document.querySelector('video');
                if (video) {
                    video.muted = true;
                    video.play().catch(err => console.log("Erro ao iniciar vídeo:", err));
                }
            } catch (e) {
                console.error("Erro JS no mute:", e);
            }
        """)

        # Retorna o navegador e a página para que possam ser fechados mais tarde
        return browser, page

    except Exception as e:
        #print(f"Erro ao abrir navegador: {e}")
        await browser.close()
        return None, None
    
# Verifica se o canal está online através da API do Twitch
async def is_channel_online(channel_name):
    try:
        # Usando uma API pública simples para verificar status do canal
        # Método alternativo sem necessidade de autenticação
        url = f"https://www.twitch.tv/{channel_name}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    #print(f"Erro ao acessar canal: Status {response.status}")
                    return False
                
                html = await response.text()
                # Se a página contém essa string específica, significa que o canal está ao vivo
                return "isLiveBroadcast" in html or "tw-channel-status-text-indicator" in html
    
    except Exception as e:
        #print(f"Erro ao verificar status do canal: {e}")
        return False

# Função para fechar o navegador se estiver aberto
async def close_browser():
    global active_browser, active_page
    
    if active_browser:
        try:
            #print("Fechando navegador...")
            await active_browser.close()
        except Exception as e:
            #print(f"Erro ao fechar navegador: {e}")
            pass
        finally:
            active_browser = None
            active_page = None

# Função principal que monitora o status e abre/fecha o navegador
async def monitor_channel():
    global active_browser, active_page
    
    #print(f"Iniciando monitoramento do canal: {CHANNEL_NAME}")
    was_online = False
    
    async with async_playwright() as playwright:
        while True:
            try:
                online = await is_channel_online(CHANNEL_NAME)
                
                if online and not was_online:
                    #print(f"Canal {CHANNEL_NAME} está online! Iniciando visualização...")
                    active_browser, active_page = await watch_twitch(CHANNEL_NAME, playwright)
                    was_online = True
                
                elif not online and was_online:
                    #print(f"Canal {CHANNEL_NAME} não está mais online. Fechando navegador.")
                    await close_browser()
                    was_online = False
                
                else:
                    status = "online" if online else "offline"
                    #print(f"Canal {CHANNEL_NAME} continua {status}. Verificando novamente em {CHECK_INTERVAL//60} minutos.")
                
                # Aguarda o intervalo definido antes da próxima verificação
                await asyncio.sleep(CHECK_INTERVAL)
                
            except Exception as e:
                #print(f"Erro no monitoramento: {e}")
                # Em caso de erro, fecha o navegador e tenta novamente após um tempo
                await close_browser()
                was_online = False
                await asyncio.sleep(60)  # Espera 1 minuto antes de tentar novamente

""" # Executa o programa
if __name__ == "__main__":
    try:
        asyncio.run(monitor_channel())
    except Exception as e:
        print(f"Erro fatal no programa: {e}") """