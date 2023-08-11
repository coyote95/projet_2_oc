import csv

from bs4 import BeautifulSoup
import requests

URL_home="http://books.toscrape.com/"
URL_page_livre="http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

def extract_data(url):
    response=requests.get(url)
    html=response.content
    return html

def save_page_html(soup,fichier):
    with open(fichier,"w")as fichier:
        fichier.write(str(soup))
        return

def title(soup):
    return soup.title.string.strip("\n")

def fichier_csv(soup):
    titre_fichier="livre1"
    with open(f"{titre_fichier}.csv","w",newline="") as fichier:
        fieldnames=["product_page_url","universal_product_code(upc)","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","img_url"]
        writer=csv.DictWriter(fichier,fieldnames=fieldnames)
        writer.writeheader()
        return

def data(soup,produit):
    th=[]
    td=[]
    for table in soup.find_all('table'):
        for tr in table.find_all("tr"):
            th.append(tr.find("th").get_text())  # colonne 1 avec header
            td.append(tr.find("td").get_text())  # colonne 2 avec valeur
    print(th)
    print(td)


def main():
    html_home=extract_data(URL_home)
    html_page_livre=extract_data(URL_page_livre)
    soup_home=BeautifulSoup(html_home,"html.parser")
    soup_livre = BeautifulSoup(html_page_livre, "html.parser")
    print(title(soup_home))
    save_page_html(soup_home,"page_home_html.txt")
    save_page_html(soup_livre, "page_livre.txt")

    fichier_csv(soup_livre)

    produit=[]

    data(soup_livre,produit)

    return

main()