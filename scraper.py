# scripts/scraper.py

import requests
from bs4 import BeautifulSoup
import json
import time
import os

# Ստեղծում ենք folder-ները
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


def get_categories():
    print("Scrapping of categories-...")
    url = 'https://books.toscrape.com/'
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    category_links = soup.select('div.side_categories ul.nav ul li a')
    categories = []
    for idx, link in enumerate(category_links, start=1):
        name = link.text.strip()
        href = link['href']
        full_url = 'https://books.toscrape.com/' + href
        categories.append({
            'category_id': idx,
            'name': name,
            'url': full_url
        })

    with open('data/raw/categories.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=4)

    print(f"Finished:  {len(categories)} categories")
    return categories


def scrape_products(categories):
    print("Start of products-scrapping...")
    all_products = []
    product_id = 1

    for cat in categories:
        page = 1
        category_id = cat['category_id']
        print(f"     category: {cat['name']}")

        while True:
            if page == 1:
                url = cat['url']
            else:
                url = cat['url'].replace('index.html', f'page-{page}.html')

            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'

            if response.status_code != 200:
                print(f"     Error at page : {url}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.find_all('article', class_='product_pod')

            if not books:
                break

            for book in books:
                title = book.h3.a['title']
                price_text = book.find('p', class_='price_color').get_text(strip=True)
                price_clean = price_text.replace('£', '').strip()
                price = float(price_clean)

                rating_class = book.find('p', class_='star-rating')['class'][1]
                rating = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}.get(rating_class, 0)

                all_products.append({
                    'product_id': product_id,
                    'name': title,
                    'price': price,
                    'rating': rating,
                    'category_id': category_id
                })
                product_id += 1

            print(f"     Page {page} —  {len(books)} book")
            page += 1
            time.sleep(1)  # polite scraping

    with open('data/raw/products.json', 'w', encoding='utf-8') as f:
        json.dump(all_products, f, ensure_ascii=False, indent=4)

    print(f"Finished: Scrapped {len(all_products)} products ")
    return all_products


if __name__ == '__main__':
    categories = get_categories()
    products = scrape_products(categories)