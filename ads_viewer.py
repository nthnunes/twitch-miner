import asyncio
import random
import requests
from playwright.async_api import async_playwright

def get_urls_from_api():
    """Busca todas as URLs da API uma única vez"""
    try:
        #print("Buscando URLs da API...")
        response = requests.get("https://twitch-miner-api.vercel.app/ads")
        urls = response.json()
        #print(f"Encontradas {len(urls)} URLs")
        return urls
    except Exception as e:
        #print(f"Erro ao buscar URLs da API: {e}")
        # URLs de fallback caso a API falhe
        return ["https://www.profitableratecpm.com/k3c6ghdvs?key=dd3be0c22f38c188264ff6a6bf2fa18a"]

async def open_link(urls):
    # Escolher URL aleatória da lista
    url = random.choice(urls)
    #print(f"URL selecionada: {url}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        
        # Aguardar entre 10 e 30 segundos na página
        wait_time = random.randint(10, 30)
        #print(f"Aguardando {wait_time} segundos...")
        await asyncio.sleep(wait_time)
        
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
