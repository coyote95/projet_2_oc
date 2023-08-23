import csv
from bs4 import BeautifulSoup
import requests
import urllib.request
import os


url_home = "http://books.toscrape.com/index.html"


def extract_html(url):

    response = requests.get(url)
    html = response.content
    return html


def fichier_csv(produit, name_csv):
    titre_fichier = name_csv
    with open(f"{titre_fichier}.csv", "w+", newline="", encoding="utf-8") as fichier:
        fieldnames = ["product_page_url", "universal_product_code(upc)", "title", "price_including_tax",
                      "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
                      "img_url"]
        writer = csv.DictWriter(fichier, fieldnames=fieldnames)
        writer.writeheader()

        for livre in produit:
            writer.writerow(livre)
        return


def data_livres(soup, produits, page):
    th = []
    td = []

    #objet dans data libre

    for table in soup.find_all('table'):
        for tr in table.find_all("tr"):
            th.append(tr.find("th").get_text())  # colonne 1 avec header
            td.append(tr.find("td").get_text())  # colonne 2 avec valeur


    h2 = soup.find('h2', string="Product Description")
    if h2:
        description_livre = h2.find_next("p").string
    else:
        description_livre = "none"


    category_in_list_breadcrumb = soup.find("ul", class_="breadcrumb").find_all('li')[2].get_text()

    image_url = soup.img["src"]

    image_url = str(image_url).replace("../", "")
    image_url_all = url_home.replace('index.html', '') + image_url
#autre fonctions

    dict_livre_info = {
        "universal_product_code(upc)": td[0],
        "price_excluding_tax": td[2],
        "price_including_tax": td[3],
        "number_available": td[5],
        "review_rating": td[6],
        "title": soup.find('h1').string,
        "product_page_url": page,
        "product_description": description_livre,
        "category": category_in_list_breadcrumb,
        "img_url": image_url_all
    }

    produits.append(dict_livre_info)

    return produits


def data_rubrique(soup, liste_rubrique):
    for li in soup.find("ul", class_="nav nav-list").find_all("li"):
        a = li.find("a")

        rubrique = a.string.strip()
        url_rubrique_relatif = str(a["href"])
        url_rubrique_absolu = url_home.replace('index.html', '') + url_rubrique_relatif
        dict_rubrique = {
            "name": rubrique,
            "url": url_rubrique_absolu,
        }
        liste_rubrique.append(dict_rubrique)

    return liste_rubrique


def download_image(image_url, save_path):
    urllib.request.urlretrieve(image_url, save_path)
    return


def all_url_livre(soup):
    liste_links = []
    for h3 in soup.find_all("h3"):
        a = h3.find("a")
        link_relatif = str(a["href"])
        link_absolu = url_home.replace('index.html', '') + str("catalogue/") + link_relatif.replace('../', "")
        liste_links.append(link_absolu)

    return liste_links



def clean_name(file_title):
    new_name = ""
    valid_chars = "-_.()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for c in file_title:

        if c in valid_chars:
            new_name += c
        else:
            new_name += "_"

    if len(new_name) > 30:
        new_name = new_name[:30]

    return new_name


def main():
    produits = []

    page_livre = []
    liste_rubrique = []

    html_home = extract_html(url_home)
    soup_home = BeautifulSoup(html_home, "html.parser")

    # ***************************        recupérer les rubriques     **********************

    liste_rubrique = data_rubrique(soup_home, liste_rubrique)
#extraction
    for rubrique in liste_rubrique[1:3]:
        produits.clear()
        page_livre.clear()
        print(rubrique.get("name"))
        name_csv = rubrique.get("name")
        url_current = rubrique.get("url")

        while True:
            html_current = extract_html(url_current)
            soup_current = BeautifulSoup(html_current, "html.parser")
            lien_next = soup_current.find("a", string="next")
            if lien_next:
                page_livre += all_url_livre(soup_current)
                url_current = url_current.replace("index.html", "") + lien_next["href"]
            else:
                page_livre += all_url_livre(soup_current)
                break

        for page in page_livre:
            print(f"la page est: {page}")
            html_page = extract_html(page)
            soup_page = BeautifulSoup(html_page, "html.parser")
            data_livres(soup_page, produits, page)
            fichier_csv(produits, name_csv)

        # *******************************     enregistrement des images     *********************

        if not os.path.exists(f"images/{name_csv}"):
            os.makedirs(f"images/{name_csv}")

        for url_livres in produits:
            url = url_livres.get("img_url")
            name_livre = url_livres.get("title")
            name_livre = clean_name(name_livre)
            image_save_path = os.path.join(f"images/{name_csv}", f"{name_livre}.jpg")
            download_image(url, image_save_path)


    return


main()
