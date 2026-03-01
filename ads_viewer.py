import asyncio
import random
import requests
import os
import sys
import time
from playwright.async_api import async_playwright
from datetime import datetime

# Fallbacks quando a API não retorna view/interval
DEFAULT_VIEW_DURATION_MIN = 10
DEFAULT_VIEW_DURATION_MAX = 60
DEFAULT_INTERVAL_MIN = 3600
DEFAULT_INTERVAL_MAX = 7200


def _parse_int(value, default):
    """Retorna value como int se for número válido, senão default."""
    if value is None:
        return default
    try:
        n = int(value)
        return n if n >= 0 else default
    except (TypeError, ValueError):
        return default


def get_ads_config_from_api():
    wait_time = 300  # Começar com 5 minutos
    max_wait_time = 7200  # Máximo de 2 horas (120 minutos)

    while True:
        try:
            response = requests.get("https://twitch-miner-api.vercel.app/ads")
            data = response.json()

            # Resposta inválida ou sem urls → tratar como vazio
            if not isinstance(data, dict):
                raise Exception("Resposta da API inválida")
            urls = data.get("urls")
            if not isinstance(urls, list) or len(urls) == 0:
                raise Exception("Lista de URLs vazia")

            view_min = _parse_int(data.get("viewDurationMin"), DEFAULT_VIEW_DURATION_MIN)
            view_max = _parse_int(data.get("viewDurationMax"), DEFAULT_VIEW_DURATION_MAX)
            interval_min = _parse_int(data.get("intervalMin"), DEFAULT_INTERVAL_MIN)
            interval_max = _parse_int(data.get("intervalMax"), DEFAULT_INTERVAL_MAX)

            # Garantir min <= max
            if view_min > view_max:
                view_min, view_max = view_max, view_min
            if interval_min > interval_max:
                interval_min, interval_max = interval_max, interval_min

            return {
                "urls": urls,
                "viewDurationMin": view_min,
                "viewDurationMax": view_max,
                "intervalMin": interval_min,
                "intervalMax": interval_max,
            }
        except Exception:
            time.sleep(wait_time)
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

async def open_link(urls, view_duration_min, view_duration_max):
    url = random.choice(urls)
    
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

        HEADLESS = True
        
        if chromium_path and os.path.exists(chromium_path):
            # Usar o Chromium empacotado
            browser = await p.chromium.launch(
                headless=HEADLESS,
                executable_path=chromium_path,
                args=args
            )
        else:
            # Usar o Chromium padrão do Playwright
            browser = await p.chromium.launch(
                headless=HEADLESS,
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
            wait_time = random.randint(view_duration_min, view_duration_max)
            await asyncio.sleep(wait_time)
            
        except Exception as e:
            print(f"{datetime.now().strftime('%d/%m/%y %H:%M:%S')} - ERROR - [ads_viewer]: Não foi possível carregar os anúncios: {e}")
            #print(f"Erro detalhado: {e}")
        
        await browser.close()

async def run_loop():
    config = get_ads_config_from_api()
    urls = config["urls"]
    view_min = config["viewDurationMin"]
    view_max = config["viewDurationMax"]
    interval_min = config["intervalMin"]
    interval_max = config["intervalMax"]

    while True:
        await open_link(urls, view_min, view_max)
        interval = random.randint(interval_min, interval_max)
        await asyncio.sleep(interval)

""" if __name__ == "__main__":
    asyncio.run(run_loop()) """
