from urllib.request import urlopen as uRequest
from bs4 import BeautifulSoup as soup
from tqdm import tqdm
import os

def scrape_page(page_url, category, page_number, _records=None):
    if _records is None:
        _records = []
    page_html = uRequest(page_url).read()
    page_soup = soup(page_html, features="html.parser")
    containers = page_soup.findAll('div', {'class': 'fx-product-list-entry'})
    for container in tqdm(containers, desc=f'Scraping page {page_number}...', total=len(containers)):
        img_url = container.findAll('a', {'class': 'product__image'})[0].picture.source.get('data-srcset', None)
        _records.append(img_url)
    return _records, category

def navigate_and_scrape(base_url, category, _records=None):
    if _records is None:
        _records = []
    all_records = _records
    page = 1
    while True:
        url = f"{base_url}?pg={page:d}&ls=25"
        records, _ = scrape_page(url, category, page)
        all_records.extend(records)
        if len(records) == 0:
            break
        next_url = f"{base_url}?pg={page + 1:d}&ls=25"
        next_records, _ = scrape_page(next_url, category, page + 1)
        if len(next_records) == 0:
            break
        page += 1
        if page > 20: # Molto probabilmente qualcosa sta andando storto, meglio salvare le immagini prese fin'ora
            break
    return all_records

listofurls = []

for url in tqdm(listofurls, desc='Processing URLs...', total=len(listofurls)):
    page_html = uRequest(url).read()
    page_soup = soup(page_html, features="html.parser")
    category_grid = page_soup.findAll('div', {'class': 'fx-category-grid'})
    if not category_grid:  # Check if category_grid is empty
        print(f"No category grid found in the URL: {url}")
        continue
    page_links = [x['href'] for x in category_grid[0].findAll('a')]
    categories = [x.text.replace('\n', '').strip() for x in category_grid[0].findAll('a')]
    for page_link, category in tqdm(zip(page_links, categories), desc='Processing pages...', total=len(page_links)):
        dest_dir = 'thomannFiato/'
        dest_dir = os.path.join(dest_dir, category)
        # Check if the directory for the category already exists
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            records = navigate_and_scrape(page_link, category)
            cats = [category] * len(records)
            print('elementi: ', len(records), len(cats))
            for i, image in tqdm(enumerate(records), desc='Saving images... in directory ' + category, total=len(records)):
                image_name = os.path.join(dest_dir, f'{i}.jpg')
                with open(image_name, 'wb') as f:
                    f.write(uRequest(image).read())

        else:
            print(f"Directory for '{category}' already exists. Skipping scraping and image download.")
