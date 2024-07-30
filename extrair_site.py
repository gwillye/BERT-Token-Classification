# Script para baixar o site da infomoney e analisar a sua estrutura

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def clean_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

def download_file(url, folder):
    filename = clean_filename(url.split('/')[-1])
    local_filename = os.path.join(folder, filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def save_html(url, folder):
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    local_html_path = os.path.join(folder, 'index.html')
    
    with open(local_html_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    
    # Download and save CSS and JS files
    for link in soup.find_all('link', {'rel': 'stylesheet'}):
        href = link.get('href')
        if href:
            css_url = urljoin(url, href)
            download_file(css_url, folder)
    
    for script in soup.find_all('script', {'src': True}):
        src = script.get('src')
        if src:
            js_url = urljoin(url, src)
            download_file(js_url, folder)
    
    print(f"Saved HTML, CSS, and JS files to {folder}")

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

if __name__ == "__main__":
    url = "https://www.infomoney.com.br/"
    folder = "site"
    create_folder(folder)
    save_html(url, folder)
