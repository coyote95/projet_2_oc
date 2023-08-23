import csv
import urllib.request
import os


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


def download_image(image_url, save_path):
    urllib.request.urlretrieve(image_url, save_path)
    return
