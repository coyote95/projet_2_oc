import requests
from bs4 import BeautifulSoup

url_home = "http://books.toscrape.com/index.html"


def extract_html(url):
    response = requests.get(url)
    if response.status_code==200:
        html = response.content
    else:
        print("fail connection!")
    return html


# fonction extract colonne 2 tableau

def tableau_colonne(soup):
    th = []
    td = []
    for table in soup.find_all('table'):
        for tr in table.find_all("tr"):
            th.append(tr.find("th").get_text())  # colonne 1 avec header
            td.append(tr.find("td").get_text())  # colonne 2 avec valeur
    return td


def description_livre(soup):
    h2 = soup.find('h2', string="Product Description")
    if h2:
        descrip_livre = h2.find_next("p").string
    else:
        descrip_livre = "none"
    return descrip_livre


def categorie(soup):
    category_in_list_breadcrumb = soup.find("ul", class_="breadcrumb").find_all('li')[2].get_text()
    return category_in_list_breadcrumb


def url_image(soup):
    image_url = soup.img["src"]
    image_url = str(image_url).replace("../", "")
    image_url_all = url_home.replace('index.html', '') + image_url
    return image_url_all


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


def all_url_livre(soup):
    liste_links = []
    for h3 in soup.find_all("h3"):
        a = h3.find("a")
        link_relatif = str(a["href"])
        link_absolu = url_home.replace('index.html', '') + str("catalogue/") + link_relatif.replace('../', "")
        liste_links.append(link_absolu)

    return liste_links


def lien_next(soup):
    return soup.find("a", string="next")
