import csv
from bs4 import BeautifulSoup
import requests
import urllib.request
import os
import extract
import transform
import load

url_home = "http://books.toscrape.com/index.html"


def main():
    produits = []
    page_livre = []
    liste_rubrique = []

    html_home = extract.extract_html(url_home)
    soup_home = BeautifulSoup(html_home, "html.parser")

    # ***************************        recupérer les rubriques     **********************

    liste_rubrique = extract.data_rubrique(soup_home, liste_rubrique)

    for rubrique in liste_rubrique[2:3]:
        produits.clear()
        page_livre.clear()
        print(rubrique.get("name"))
        name_csv = rubrique.get("name")
        url_current = rubrique.get("url")

        while True:
            html_current = extract.extract_html(url_current)
            soup_current = BeautifulSoup(html_current, "html.parser")

            if extract.lien_next(soup_current):
                page_livre += extract.all_url_livre(soup_current)
                url_current = url_current.replace("index.html", "") + extract.lien_next(soup_current)["href"]
                print(url_current)
            else:
                page_livre += extract.all_url_livre(soup_current)
                break

        for page in page_livre:
            print(f"la page est: {page}")
            html_page = extract.extract_html(page)
            soup_page = BeautifulSoup(html_page, "html.parser")
            print(soup_page)
            transform.data_livres(soup_page,produits, page)
            load.fichier_csv(produits, name_csv)

        # *******************************     enregistrement des images     *********************

        if not os.path.exists(f"images/{name_csv}"):
            os.makedirs(f"images/{name_csv}")

        for url_livres in produits:
            url = url_livres.get("img_url")
            name_livre = url_livres.get("title")
            name_livre = transform.clean_name(name_livre)
            image_save_path = os.path.join(f"images/{name_csv}", f"{name_livre}.jpg")
            load.download_image(url, image_save_path)

    return


if __name__ == '__main__':
    main()
