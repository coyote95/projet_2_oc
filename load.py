import csv
import urllib.request
import os


# Function to create a CSV file with book data
def csv_file(products, csv_name):
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
    urllib.request.urlretrieve(image_url, save_path)
    return
