import asyncio
import random
import requests
import os
import sys
import time
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime

# Fallbacks quando a API não retorna view/interval
DEFAULT_VIEW_DURATION_MIN = 10
DEFAULT_VIEW_DURATION_MAX = 60
DEFAULT_INTERVAL_MIN = 3600
DEFAULT_INTERVAL_MAX = 7200
DEFAULT_AD_LOAD_TIMEOUT_MS = 15000
DEFAULT_CLICK_DELAY_MIN = 2
DEFAULT_CLICK_DELAY_MAX = 6


def _parse_int(value, default):
    """Retorna value como int se for número válido, senão default."""
    if value is None:
        return default
    try:
        n = int(value)
        return n if n >= 0 else default
    except (TypeError, ValueError):
        return default


def _parse_click_chance(value):
    """Retorna chance de clique entre 0 e 100."""
    if value is None:
        return 0
    try:
        chance = int(value)
        return max(0, min(100, chance))
    except (TypeError, ValueError):
        return 0


def _normalize_ad_slots(raw_slots, default_click_chance=0):
    """Normaliza slots vindos da API para [{slot, clickChance}, ...]."""
    if not isinstance(raw_slots, list):
        return []

    slots = []
    for item in raw_slots:
        if not isinstance(item, dict):
            continue

        slot = _parse_int(item.get("slot"), None)
        if slot is None:
            slot = _parse_int(item.get("index"), None)
        if slot is None or slot <= 0:
            continue

        click_chance = _parse_click_chance(item.get("clickChance"))
        if click_chance == 0:
            click_chance = _parse_click_chance(item.get("click_chance"))
        if click_chance == 0 and default_click_chance > 0:
            click_chance = default_click_chance

        slots.append({"slot": slot, "clickChance": click_chance})

    return sorted(slots, key=lambda item: item["slot"])


def _normalize_pages(data):
    """
    Aceita o novo formato `pages` ou o legado `urls`.
    Cada página retorna: {url, ads: [{slot, clickChance}, ...]}.
    """
    default_click_chance = _parse_click_chance(data.get("defaultClickChance"))
    default_slots = _normalize_ad_slots(
        data.get("defaultAds") or data.get("default_ad_slots"),
        default_click_chance,
    )

    pages = []
    raw_pages = data.get("pages")
    if isinstance(raw_pages, list) and len(raw_pages) > 0:
        for page in raw_pages:
            if not isinstance(page, dict):
                continue

            url = page.get("url")
            if not isinstance(url, str) or not url.strip():
                continue

            page_slots = _normalize_ad_slots(
                page.get("ads") or page.get("slots"),
                default_click_chance,
            )
            if not page_slots and default_slots:
                page_slots = default_slots

            pages.append({"url": url.strip(), "ads": page_slots})
        return pages

    urls = data.get("urls")
    if isinstance(urls, list):
        for url in urls:
            if not isinstance(url, str) or not url.strip():
                continue
            pages.append({"url": url.strip(), "ads": default_slots})

    return pages


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
            pages = _normalize_pages(data)
            if len(pages) == 0:
                raise Exception("Lista de páginas vazia")

            view_min = _parse_int(data.get("viewDurationMin"), DEFAULT_VIEW_DURATION_MIN)
            view_max = _parse_int(data.get("viewDurationMax"), DEFAULT_VIEW_DURATION_MAX)
            interval_min = _parse_int(data.get("intervalMin"), DEFAULT_INTERVAL_MIN)
            interval_max = _parse_int(data.get("intervalMax"), DEFAULT_INTERVAL_MAX)

            # Garantir min <= max
            if view_min > view_max:
                view_min, view_max = view_max, view_min
            if interval_min > interval_max:
                interval_min, interval_max = interval_max, interval_min

            ad_load_timeout_ms = _parse_int(
                data.get("adLoadTimeoutMs"),
                DEFAULT_AD_LOAD_TIMEOUT_MS,
            )
            click_delay_min = _parse_int(
                data.get("clickDelayMin"),
                DEFAULT_CLICK_DELAY_MIN,
            )
            click_delay_max = _parse_int(
                data.get("clickDelayMax"),
                DEFAULT_CLICK_DELAY_MAX,
            )
            if click_delay_min > click_delay_max:
                click_delay_min, click_delay_max = click_delay_max, click_delay_min

            return {
                "pages": pages,
                "viewDurationMin": view_min,
                "viewDurationMax": view_max,
                "intervalMin": interval_min,
                "intervalMax": interval_max,
                "adLoadTimeoutMs": ad_load_timeout_ms,
                "clickDelayMin": click_delay_min,
                "clickDelayMax": click_delay_max,
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


def _should_click_ad(click_chance):
    return click_chance > 0 and random.randint(1, 100) <= click_chance


async def _try_click_ad_slot(context, page, slot, click_chance, ad_load_timeout_ms):
    if not _should_click_ad(click_chance):
        return False

    slot_locator = page.locator(f'[data-ad-slot="{slot}"]')
    try:
        await slot_locator.wait_for(state="attached", timeout=ad_load_timeout_ms)
        await slot_locator.scroll_into_view_if_needed()

        iframe = slot_locator.locator("iframe").first
        if await iframe.count() > 0:
            await iframe.wait_for(state="visible", timeout=ad_load_timeout_ms)
            click_target = iframe
        else:
            click_target = slot_locator

        try:
            async with context.expect_page(timeout=8000) as new_page_info:
                await click_target.click(timeout=5000)
            await new_page_info.value
        except PlaywrightTimeoutError:
            pass

        await page.bring_to_front()
        return True
    except Exception as e:
        print(
            f"{datetime.now().strftime('%d/%m/%y %H:%M:%S')} - WARN - [ads_viewer]: "
            f"Não foi possível clicar no anúncio {slot}: {e}"
        )
        return False


async def _maybe_click_ads(context, page, ads, ad_load_timeout_ms, click_delay_min, click_delay_max):
    if not ads:
        return

    for ad in ads:
        clicked = await _try_click_ad_slot(
            context,
            page,
            ad["slot"],
            ad["clickChance"],
            ad_load_timeout_ms,
        )
        if clicked:
            delay = random.randint(click_delay_min, click_delay_max)
            await asyncio.sleep(delay)


async def open_link(
    page_config,
    view_duration_min,
    view_duration_max,
    ad_load_timeout_ms,
    click_delay_min,
    click_delay_max,
):
    url = page_config["url"]
    ads = page_config.get("ads", [])
    
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
            view_duration = random.randint(view_duration_min, view_duration_max)
            start_time = time.monotonic()

            await page.goto(url, wait_until="domcontentloaded")
            await _maybe_click_ads(
                context,
                page,
                ads,
                ad_load_timeout_ms,
                click_delay_min,
                click_delay_max,
            )

            elapsed = time.monotonic() - start_time
            remaining = max(0, view_duration - elapsed)
            if remaining > 0:
                await asyncio.sleep(remaining)
            
        except Exception as e:
            print(f"{datetime.now().strftime('%d/%m/%y %H:%M:%S')} - ERROR - [ads_viewer]: Não foi possível carregar os anúncios: {e}")
            #print(f"Erro detalhado: {e}")
        
        await browser.close()

async def run_loop():
    config = get_ads_config_from_api()
    pages = config["pages"]
    view_min = config["viewDurationMin"]
    view_max = config["viewDurationMax"]
    interval_min = config["intervalMin"]
    interval_max = config["intervalMax"]
    ad_load_timeout_ms = config["adLoadTimeoutMs"]
    click_delay_min = config["clickDelayMin"]
    click_delay_max = config["clickDelayMax"]

    while True:
        page_config = random.choice(pages)
        await open_link(
            page_config,
            view_min,
            view_max,
            ad_load_timeout_ms,
            click_delay_min,
            click_delay_max,
        )
        interval = random.randint(interval_min, interval_max)
        await asyncio.sleep(interval)

""" if __name__ == "__main__":
    asyncio.run(run_loop()) """
