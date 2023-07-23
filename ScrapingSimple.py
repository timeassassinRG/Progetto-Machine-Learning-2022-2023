from urllib.request import urlopen as uRequest
from bs4 import BeautifulSoup as soup
from tqdm import tqdm
import os

def scrape_page(page_url, _records=None):
    if _records is None:
        _records = []
    page_html = uRequest(page_url).read()
    page_soup = soup(page_html, features="html.parser")
    containers = page_soup.findAll('div', {'class': 'fx-product-list-entry'})
    for container in tqdm(containers, desc='Scraping page...', total=len(containers)):
        img_url = container.findAll('a', {'class': 'product__image'})[0].picture.source.get('data-srcset', None)
        _records.append(img_url)
    return _records

def navigate_and_scrape(base_url, records=None):
    if records is None:
        records = []
    all_records = records
    page = 1
    while True:
        url = f"{base_url}?pg={page:d}&ls=25"
        records = scrape_page(url)
        all_records.extend(records)
        if len(records) == 0:
            break
        page += 1
    return all_records

url = ['https://www.thomann.de/it/modelli_st.html']
records = navigate_and_scrape(url)
cats = []
cats.extend(['modelli_st']*len(records))
print('elementi: ', len(records), len(cats))
#save images
dest_dir = 'thomann/'
dest_dir = os.path.join(dest_dir, 'modelli_st')
os.makedirs(dest_dir, exist_ok=True)
for i, image in tqdm(enumerate(records), desc='Saving images...', total=len(records)):
    image_name = os.path.join(dest_dir, f'{i}.jpg')
    with open(image_name, 'wb') as f:
        f.write(uRequest(image).read())