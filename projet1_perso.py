import csv
from bs4 import BeautifulSoup
import requests
import urllib.request
import os

URL_home = "http://books.toscrape.com/"
URL_page_livre = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"


def extract_data(url):
    response = requests.get(url)
    html = response.content
    return html


def save_page_html(soup, fichier):
    with open(fichier, "w") as fichier:
        fichier.write(str(soup))
        return


def title(soup):
    return soup.title.string.strip("\n")


def fichier_csv(soup, produit):
    titre_fichier = "livre1"
    with open(f"{titre_fichier}.csv", "w", newline="") as fichier:
        fieldnames = ["product_page_url", "universal_product_code(upc)", "title", "price_including_tax",
                      "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
                      "img_url"]
        writer = csv.DictWriter(fichier, fieldnames=fieldnames)
        writer.writeheader()

        for livre in produit:
            writer.writerow(livre)
        return


def data(soup, produit):
    th = []
    td = []
    for table in soup.find_all('table'):
        for tr in table.find_all("tr"):
            th.append(tr.find("th").get_text())  # colonne 1 avec header
            td.append(tr.find("td").get_text())  # colonne 2 avec valeur

    description_livre = soup.find('h2', string="Product Description").find_next("p").string

    category_in_list_breadcrumb = soup.find("ul", class_="breadcrumb").find_all('li')[2].get_text()

    image_url = soup.img["src"]
    image_url = str(image_url).replace("../../", "")
    image_url_all = URL_home + image_url

    print(f'url de image:{image_url_all}')

    print(category_in_list_breadcrumb)

    dict_livre_info = {
        "universal_product_code(upc)": td[0],
        "price_excluding_tax": td[2],
        "price_including_tax": td[3],
        "number_available": td[5],
        "review_rating": td[6],
        "title": soup.find('h1').string,
        "product_page_url": URL_page_livre,
        "product_description": description_livre,
        "category": category_in_list_breadcrumb,
        "img_url": image_url_all
    }

    # print(description_livre)
    # print(soup.find('h1').string)
    # print(th)
    # print(td)
    produit.append(dict_livre_info)

    return produit


def download_image(image_url, save_path):
    urllib.request.urlretrieve(image_url, save_path)
    return


def main():
    html_home = extract_data(URL_home)
    html_page_livre = extract_data(URL_page_livre)
    soup_home = BeautifulSoup(html_home, "html.parser")
    soup_livre = BeautifulSoup(html_page_livre, "html.parser")
    print(title(soup_home))
    save_page_html(soup_home, "page_home_html.txt")
    save_page_html(soup_livre, "page_livre.txt")

    produit = []

    livre = data(soup_livre, produit)
    fichier_csv(soup_livre, produit)

    if not os.path.exists('images'):
        os.makedirs('images')

    url_livres = livre[0].get("img_url")
    name_livres = livre[0].get("title")

    image_save_path = os.path.join('images', f"{name_livres}.jpg")
    print(image_save_path)

    download_image(url_livres, image_save_path)

    return


main()
