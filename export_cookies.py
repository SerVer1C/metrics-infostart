"""
Скрипт для экспорта cookies из Chrome в JSON.
Использование:
    python export_cookies.py > cookies.json
    
Затем скопируйте содержимое cookies.json в GitHub Secrets 
как INFOSTART_COOKIES в личный репозиторий,
который использует action для обновления списка статей.
"""
import os
import sys
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def export_cookies():
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    
    profile_dir = os.path.join(os.getcwd(), 'infostart_profile')
    chrome_options.add_argument(f'--user-data-dir={profile_dir}')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get('https://infostart.ru')
        time.sleep(5)
        
        cookies = driver.get_cookies()
        infostart_cookies = [c for c in cookies if 'infostart.ru' in c.get('domain', '')]
        
        print(json.dumps(infostart_cookies, ensure_ascii=False, indent=2))
        print(f'\n[INFO] Экспортировано {len(infostart_cookies)} cookies для infostart.ru', file=sys.stderr)
        
    finally:
        driver.quit()


if __name__ == '__main__':
    export_cookies()
