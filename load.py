import csv
import urllib.request


"""
Module for load:    -data in csv file 
                    -load image
"""


def csv_file(products, csv_name):
    """
    create a CSV file with book data
    :param products: (list of dict)
    :param csv_name: (str)
    :return:None

    """
    file_title = csv_name
    with open(f"{file_title}.csv", "w+", newline="", encoding="utf-8") as fichier:
        fieldnames = ["product_page_url", "universal_product_code(upc)", "title", "price_including_tax",
                      "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
                      "img_url"]
        writer = csv.DictWriter(fichier, fieldnames=fieldnames)
        writer.writeheader()

        for book in products:
            writer.writerow(book)
        return


# Function to download an image from a URL and save it to a specified path
def download_image(image_url, save_path):
    """
    Download an image from a URL and save it to a specified path.
    :param image_url: (str)
    :param save_path: (str)
    :return: none
    """
    urllib.request.urlretrieve(image_url, save_path)
    return
