import csv
from bs4 import BeautifulSoup
import requests
import urllib.request
import os

URL_home = "http://books.toscrape.com/index.html"
URL_current="http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
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
    with open(f"{titre_fichier}.csv", "w+", newline="",encoding="utf-8") as fichier:
        fieldnames = ["product_page_url", "universal_product_code(upc)", "title", "price_including_tax",
                      "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
                      "img_url"]
        writer = csv.DictWriter(fichier, fieldnames=fieldnames)
        writer.writeheader()

        for livre in produit:
            writer.writerow(livre)
        return


def data(soup, produits, page):
    th = []
    td = []
    print(page)
    for table in soup.find_all('table'):
        for tr in table.find_all("tr"):
            th.append(tr.find("th").get_text())  # colonne 1 avec header
            td.append(tr.find("td").get_text())  # colonne 2 avec valeur

    description_livre = soup.find('h2', string="Product Description").find_next("p").string

    category_in_list_breadcrumb = soup.find("ul", class_="breadcrumb").find_all('li')[2].get_text()

    image_url = soup.img["src"]
    image_url = str(image_url).replace("../../", "")
    image_url_all = URL_home + image_url

    # print(f'url de image:{image_url_all}')
    # print(category_in_list_breadcrumb)

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


def download_image(image_url, save_path):
    urllib.request.urlretrieve(image_url, save_path)
    return


def all_url_livre(soup):
    liste_links = []
    for h3 in soup.find_all("h3"):
        #  print(f"le titre H3 est:{h3}")
        a = h3.find("a")
        link_relatif = str(a["href"])
        #print (f"URL home :{URL_home}")
        #print(link_relatif)
        link_absolu = URL_home.replace('index.html','')+str("catalogue/")+link_relatif.replace('../',"")

        #print(f'lien absolu:{link_absolu}')
        # print(f"le titre href est:{link_absolu}")
        liste_links.append(link_absolu)


    return liste_links


def main():
    produits = []
    html_home = extract_data(URL_home)
    soup_home = BeautifulSoup(html_home, "html.parser")

    html_current=html_home

    soup_current=soup_home

    URL_current = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
    url_home_page = URL_current.replace('index.html', "")

    # page_livre = all_url_livre(soup_home)
    #
    # for page in page_livre:
    #     html_page = extract_data(page)
    #     soup_page = BeautifulSoup(html_page, "html.parser")
    #     # save_page_html(soup_home, "page_home_html.txt")
    #     # save_page_html(soup_page, "page_livre.txt")
    #     data(soup_page, produits, page)
    #     fichier_csv(soup_page, produits)




    #
    # while True:
    #
    #     html_current=extract_data(url_current)
    #     soup_current = BeautifulSoup(html_current, "html.parser")
    #     lien_next = soup_current.find("a", string="next")
    #
    #     if lien_next:
    #         soup_current = BeautifulSoup(html_current, "html.parser")
    #
    #         current_url = requests.get(url_current).url
    #         html_next = extract_data(current_url)
    #         soup_next = BeautifulSoup(html_next, "html.parser")
    #         soup_current = soup_next
    #         print(current_url)
    #
    #         lien_next = soup_current.find("a", string="next")
    #         url_current = url_home_page + lien_next["href"]
    #
    #         html_current = extract_data(url_current)
    #
    #         print(lien_next)
    #
    #
    #     else:
    #         break

    while True:

        html_current = extract_data(URL_current)
        soup_current = BeautifulSoup(html_current, "html.parser")
        lien_next = soup_current.find("a", string="next")

        if lien_next:

            page_livre = all_url_livre(soup_current)
           # print(f"page livre:{page_livre}")
            for page in page_livre:
                html_page = extract_data(page)
                soup_page = BeautifulSoup(html_page, "html.parser")
                print(f'la page est: {page}')
                data(soup_page, produits, page)
                fichier_csv(soup_current, produits)


            URL_current = url_home_page + lien_next["href"]
            print(URL_current)
            print(lien_next)

        else:
            print('erreur:')
            print(URL_current)
            print(lien_next)
            break

    ########################      enregistrement des images     ###################

    # if not os.path.exists('images'):
    #     os.makedirs('images')
    #
    # for url_livres in produits:
    #     # {print(url_livres.get("title"))
    #
    #     url = url_livres.get("img_url")
    #     name_livre = url_livres.get("title")
    #
    #     image_save_path = os.path.join('images', f"{name_livre}.jpg")
    #     # print(image_save_path)
    #
    #     # download_image(url, image_save_path)
    #
    # # print (page_livre)

    return


main()
