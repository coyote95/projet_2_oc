import csv
from bs4 import BeautifulSoup
import requests
import urllib.request
import os
import extract
import transform
import load

url_home = "http://books.toscrape.com/index.html"
url_home_relatif = transform.delete_url_index(url_home)


def main():
    produits = []
    page_livre = []
    liste_rubrique = []

    html_home = extract.extract_html(url_home)
    soup_home = BeautifulSoup(html_home, "html.parser")

    # ***************************        recupérer les rubriques     **********************

    liste_rubrique = extract.data_rubrique(soup_home, liste_rubrique, url_home_relatif)

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
                url_current = transform.delete_url_index(url_current) + extract.lien_next(soup_current)["href"]
                print(url_current)
            else:
                page_livre += extract.all_url_livre(soup_current)
                break

        for page in page_livre:
            print(f"la page est: {page}")
            html_page = extract.extract_html(page)
            soup_page = BeautifulSoup(html_page, "html.parser")
            transform.data_livres(soup_page, produits, page)
            load.fichier_csv(produits, name_csv)

        # *******************************     enregistrement des images     *********************

        if not os.path.exists(f"images/{name_csv}"):
            os.makedirs(f"images/{name_csv}")

        for produit in produits:
            url_img = produit.get("img_url")
            name_livre = produit.get("title")
            name_livre = transform.clean_name(name_livre)
            image_save_path = os.path.join(f"images/{name_csv}", f"{name_livre}.jpg")
            load.download_image(url_img, image_save_path)

    return


if __name__ == '__main__':
    main()
