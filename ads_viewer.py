import asyncio
import random
import requests
import os
import sys
import time
from playwright.async_api import async_playwright
from datetime import datetime

def get_urls_from_api():
    wait_time = 300  # Começar com 5 minutos
    max_wait_time = 7200  # Máximo de 2 horas (120 minutos)
    
    while True:
        try:
            #print(f"{datetime.now().strftime('%d/%m/%y %H:%M:%S')} - INFO - [ads_viewer]: Buscando URLs da API...")
            response = requests.get("https://twitch-miner-api.vercel.app/ads")
            urls = response.json()
            
            # Verificar se o vetor não está vazio
            if urls and len(urls) > 0:
                #print(f"{datetime.now().strftime('%d/%m/%y %H:%M:%S')} - INFO - [ads_viewer]: Encontradas {len(urls)} URLs")
                return urls
            else:
                #print(f"{datetime.now().strftime('%d/%m/%y %H:%M:%S')} - WARNING - [ads_viewer]: API retornou lista vazia")
                raise Exception("Lista de URLs vazia")
                
        except Exception as e:
            #print(f"{datetime.now().strftime('%d/%m/%y %H:%M:%S')} - ERROR - [ads_viewer]: Erro ao buscar URLs da API: {e}")
            #print(f"{datetime.now().strftime('%d/%m/%y %H:%M:%S')} - INFO - [ads_viewer]: Tentando novamente em {wait_time//60} minutos...")
            
            time.sleep(wait_time)
            
            # Dobrar o tempo de espera para a próxima tentativa, respeitando o máximo
            wait_time = min(wait_time * 2, max_wait_time)

def get_chromium_path():
    """Retorna o caminho do Chromium baseado se está executando como executável ou script"""
    if getattr(sys, 'frozen', False):
        # Executando como executável PyInstaller
        exe_dir = os.path.dirname(sys.executable)
        chromium_path = os.path.join(exe_dir, "browsers", "chromium-1161", "chrome-win", "chrome.exe")
    else:
        # Executando como script Python normal
        chromium_path = None  # Deixa o Playwright usar o padrão
    
    return chromium_path

async def open_link(urls):
    # Escolher URL aleatória da lista
    url = random.choice(urls)
    #print(f"URL selecionada: {url}")
    
    async with async_playwright() as p:
        chromium_path = get_chromium_path()
        
        # Argumentos para mascarar o modo headless
        args = [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-field-trial-config',
            '--disable-ipc-flooding-protection',
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-default-apps'
        ]
        
        if chromium_path and os.path.exists(chromium_path):
            # Usar o Chromium empacotado
            browser = await p.chromium.launch(
                headless=True,
                executable_path=chromium_path,
                args=args
            )
        else:
            # Usar o Chromium padrão do Playwright
            browser = await p.chromium.launch(
                headless=True,
                args=args
            )
        
        # Criar contexto com configurações que mascaram automação
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='pt-BR',
            timezone_id='America/Sao_Paulo'
        )
        
        page = await context.new_page()
        
        # Remover propriedades que indicam automação
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['pt-BR', 'pt', 'en'],
            });
            
            window.chrome = {
                runtime: {},
            };
            
            Object.defineProperty(navigator, 'permissions', {
                get: () => ({
                    query: () => Promise.resolve({ state: 'granted' }),
                }),
            });
        """)
        
        try:
            await page.goto(url)
            
            # Aguardar entre 10 e 30 segundos na página
            wait_time = random.randint(10, 30)
            #print(f"Aguardando {wait_time} segundos...")
            await asyncio.sleep(wait_time)
            
        except Exception as e:
            print(f"{datetime.now().strftime('%d/%m/%y %H:%M:%S')} - ERROR - [ads_viewer]: Não foi possível carregar os anúncios: {e}")
            #print(f"Erro detalhado: {e}")
        
        await browser.close()

async def run_loop():
    # Buscar URLs da API apenas uma vez
    urls = get_urls_from_api()
    
    while True:
        #print("Abrindo página...")
        await open_link(urls)
        
        # Aguardar entre 30 segundos e 1 minuto e meio antes de repetir
        interval = random.randint(30, 60)
        #print(f"Aguardando {interval%60} segundos para próxima execução...")
        await asyncio.sleep(interval)

""" if __name__ == "__main__":
    asyncio.run(run_loop()) """
