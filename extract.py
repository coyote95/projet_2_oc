import requests
from bs4 import BeautifulSoup


def extract_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.content
    else:
        print("Connection failed!")
        html = 0
    return html


# fonction extract colonne 2 tableau

def column_table(soup):
    th = []
    td = []
    for table in soup.find_all('table'):
        for tr in table.find_all("tr"):
            th.append(tr.find("th").get_text())  # Column 1 with header
            td.append(tr.find("td").get_text())  # Column 2 with values
    return td


def book_description(soup):
    h2 = soup.find('h2', string="Product Description")
    if h2:
        book_description_paragraph = h2.find_next("p").string
    else:
        book_description_paragraph = "none"
    return book_description_paragraph


def book_category(soup):
    category_list = soup.find("ul", class_="breadcrumb").find_all('li')[2].get_text()
    return category_list


def url_image(soup, url_home_relatif):
    image_url = str(soup.img["src"]).replace("../", "")
    image_url_all = url_home_relatif + image_url
    return image_url_all


def all_categories(soup, category_list, relative_home_url):
    for li in soup.find("ul", class_="nav nav-list").find_all("li"):
        a = li.find("a")
        category_name = a.string.strip()
        category_relative_url = str(a["href"])
        category_absolute_url = relative_home_url + category_relative_url
        category_dict = {
            "name": category_name,
            "url": category_absolute_url,
        }
        category_list.append(category_dict)

    return category_list


def all_book_urls(soup, url_home_relatif):
    all_links = []
    for h3 in soup.find_all("h3"):
        a = h3.find("a")
        relatif_link = str(a["href"])
        absolute_link = url_home_relatif + str("catalogue/") + relatif_link.replace('../', "")
        all_links.append(absolute_link)

    return all_links


def next_link(soup):
    return soup.find("a", string="next")
