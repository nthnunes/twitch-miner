from playwright.sync_api import sync_playwright
import time
import os
import glob
import pickle
import requests
from datetime import datetime

def check_streamer_online(channel_name):
    """Check if a streamer is online using Twitch API"""
    try:
        # Using a simple public API to check channel status
        url = f"https://www.twitch.tv/{channel_name}"
        
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return False
        
        html = response.text
        # If the page contains these specific strings, it means the channel is live
        is_online = "isLiveBroadcast" in html or "tw-channel-status-text-indicator" in html
        
        return is_online
    
    except Exception as e:
        return False

def load_cookies_from_pkl(file_path):
    """Load cookies from a .pkl (pickle) file from Twitch Miner"""
    try:
        with open(file_path, 'rb') as f:
            cookies_data = pickle.load(f)
        
        # Convert pickle format to the format that Playwright expects
        playwright_cookies = []
        for cookie in cookies_data:
            if isinstance(cookie, dict) and 'name' in cookie and 'value' in cookie:
                playwright_cookie = {
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'domain': '.twitch.tv',  # Default Twitch domain
                    'path': '/'
                }
                playwright_cookies.append(playwright_cookie)
        
        return playwright_cookies
    except Exception as e:
        return []

def inject_cookies(page, cookies):
    """Inject cookies into the browser"""
    if cookies:
        page.context.add_cookies(cookies)

def open_browsers_for_all_accounts(playwright, pkl_files, channel_name):
    """Open browsers for all accounts when the channel is online"""
    browsers = []
    
    for cookie_file in pkl_files:
        try:
            cookies = load_cookies_from_pkl(cookie_file)
            
            # Start the browser
            browser = playwright.firefox.launch(headless=False)
            page = browser.new_page()
            
            # Inject cookies for this specific account
            inject_cookies(page, cookies)
            
            # Access the URL
            page.goto(f"https://www.twitch.tv/{channel_name}")
            
            browsers.append(browser)
            
        except Exception as e:
            pass
    
    return browsers

def close_all_browsers(browsers):
    """Close all browsers"""
    if browsers:
        for browser in browsers:
            browser.close()

def monitor_channel():
    # Folder where cookie files are located
    COOKIES_FOLDER = "cookies"
    
    # Twitch channel to monitor
    CHANNEL_NAME = "boimoraes"
    
    # Check interval when offline (5 minutes)
    CHECK_INTERVAL = 300  # 5 minutes in seconds
    
    # Check if folder exists
    if not os.path.exists(COOKIES_FOLDER):
        print("aqui")
        return
    
    # List only .pkl files
    pkl_files = glob.glob(os.path.join(COOKIES_FOLDER, "*.pkl"))
    
    if not pkl_files:
        return
    
    with sync_playwright() as p:
        browsers = []
        is_online = False
        
        try:
            while True:
                current_status = check_streamer_online(CHANNEL_NAME)
                
                if current_status and not is_online:
                    # Streamer went online - open all browsers
                    print(f"{datetime.now().strftime('%d/%m/%y %H:%M:%S')} - INFO - [twitch_viewer]: Iniciando navegador para assistir o canal: {CHANNEL_NAME}")
                    browsers = open_browsers_for_all_accounts(p, pkl_files, CHANNEL_NAME)
                    is_online = True
                    
                elif not current_status and is_online:
                    # Streamer went offline - close all browsers
                    close_all_browsers(browsers)
                    browsers = []
                    is_online = False
                    
                # Wait for the defined interval before next check
                if is_online:
                    # If online, check every minute
                    time.sleep(60)
                else:
                    # If offline, check every 5 minutes
                    time.sleep(CHECK_INTERVAL)
                    
        except KeyboardInterrupt:
            close_all_browsers(browsers)

""" if __name__ == "__main__":
    monitor_channel() """
