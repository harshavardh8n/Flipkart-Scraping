import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

def scrape_flipkart(page_range):
    product_name = []
    product_price = []
    product_desc = []
    product_reviews = []
    product_images = []
    product_link = []

    for i in range(page_range[0], page_range[1] + 1):
        url = f"https://www.flipkart.com/search?q=mobiles+under+40K&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={i}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")

        box = soup.find("div", class_="DOjaWF gdgoEp")
        if not box:
            continue

        names = box.find_all("div", class_="KzDlHZ")
        prices = box.find_all("div", class_="Nx9bqj")
        reviews = box.find_all("div", class_="XQDdHH")
        images = box.find_all("div", class_="_4WELSP")
        descs = box.find_all("ul", class_="G4BRas")
        links = box.find_all("a", class_="CGtC98")

        for i in range(len(names)):
            product_name.append(names[i].text if i < len(names) else "N/A")
            product_price.append(prices[i].text if i < len(prices) else "N/A")
            product_reviews.append(reviews[i].text if i < len(reviews) else "N/A")
            product_desc.append(descs[i].text if i < len(descs) else "N/A")
            img_tag = images[i].find("img") if i < len(images) else None
            img_src = img_tag.get("src") if img_tag else "N/A"
            product_images.append(img_src)
            linksc = links[i].get("href") if i < len(links) else "#"
            product_link.append("https://www.flipkart.com" + linksc)

    products = []
    for i in range(len(product_name)):
        products.append({
            "Product Name": product_name[i],
            "Price": product_price[i],
            "Product Image": product_images[i],
            "Description": product_desc[i],
            "Reviews": product_reviews[i],
            "Product Link": product_link[i]
        })

    return products

def save_to_csv_and_json(products, csv_filename, json_filename):
    df = pd.DataFrame(products)
    df.to_csv(csv_filename, index=False)
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(products, json_file, indent=4, ensure_ascii=False)

flipkart_data = scrape_flipkart((1, 10))
save_to_csv_and_json(flipkart_data, "scraped_flipkart_data.csv", "products.json")
