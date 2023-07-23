import requests
from bs4 import BeautifulSoup
import os
import urllib
import re

def sanitize_filename(filename):
    # Rimuovi caratteri non alfanumerici e sostituiscili con un underscore
    return re.sub(r'\W+', '_', filename)

def scrape_images(url, output_folder):
    # Fai richiesta alla pagina web
    response = requests.get(url)
    if response.status_code != 200:
        print("Errore nella richiesta HTTP:", response.status_code)
        return
    
    # Crea la cartella di output se non esiste già
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Parsing dell'HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Trova tutte le thumbnail delle chitarre nella pagina
    thumbnails = soup.find_all('img', class_='loaded')
    
    for thumbnail in thumbnails:
        # Ottieni l'URL dell'immagine di dimensioni maggiori
        img_url = thumbnail['data-original']
        
        # Estrai il nome del file dal percorso dell'immagine
        img_filename = os.path.basename(img_url)
        
        # Sanitizza il nome del file
        img_filename = sanitize_filename(img_filename)
        
        # Scarica l'immagine e salvala nella cartella di output
        output_path = os.path.join(output_folder, img_filename)
        
        try:
            urllib.request.urlretrieve(img_url, output_path)
            print("Scaricata:", img_filename)
        except urllib.error.HTTPError as e:
            print("Errore durante il download di", img_filename, ":", e.code)

# URL della pagina principale
main_url = 'https://www.guitarcenter.com/Acoustic-Guitars.gc?N=18153+1051&icid=LP2465#pageName=category-page&N=18153+1051+1051&Nao=0&recsPerPage=90&&Ns=pHL&postalCode=07030&radius=100&profileCountryCode=US&profileCurrencyCode=USD'

# Percorso della cartella contenente le immagini scaricate
output_folder = 'Guitar'

# Scarica le immagini dalla pagina principale
scrape_images(main_url, output_folder)

# Effettua lo scraping delle pagine successive, se disponibili
for page_number in range(2, 7):  # 6 pagine successive
    next_page_url = f'https://www.example.com/Acoustic-Guitars?page={page_number}'
    scrape_images(next_page_url, output_folder)

print("Scaricamento completato.")