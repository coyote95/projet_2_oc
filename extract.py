import requests
import time

"""
    Module for extract data from HTML content

"""


def extract_html(url):
    """
    Extract html code
    :param url: (str)
    :return: (str) html code
    """
    response = requests.get(url)
    if response.status_code == 200:
        time.sleep(0.1)
        html = response.content
    else:
        print("Connection failed!")
        html = "0"
    return html


def review_rating(soup):
    """
    Extract review rating
    :param soup: BeautifulSoup object
    :return: number (str)
    """
    star = soup.find("p", class_="star-rating")
    if star:
        number_star = star["class"][1]
        return number_star


def column_table(soup):
    """
    Extracts data from the second column of a table
    :param soup: BeautifulSoup object
    :return: list of second collumn value
    """
    th = []
    td = []
    for table in soup.find_all('table'):
        for tr in table.find_all("tr"):
            th.append(tr.find("th").get_text())  # Column 1 with header
            td.append(tr.find("td").get_text())  # Column 2 with values
    return td


def book_description(soup):
    """
    Extract paragraph with book description
    :param soup: BeautifulSoup object
    :return: paragraph with book description
    """
    h2 = soup.find('h2', string="Product Description")
    if h2:
        book_description_paragraph = h2.find_next("p").string
    else:
        book_description_paragraph = "none"
    return book_description_paragraph


def book_category(soup):
    """
    Extract book category
    :param soup: BeautifulSoup object
    :return:(str) category
    """
    category = soup.find("ul", class_="breadcrumb").find_all('li')[2].get_text()
    return category


def url_image(soup, url_home_relatif):
    """
    Extract url image
    :param soup: BeautifulSoup object
    :param url_home_relatif: (str)
    :return: (str) url absolute image
    """
    image_url_relatif = str(soup.img["src"]).replace("../", "")
    image_url_absolute = url_home_relatif + image_url_relatif
    return image_url_absolute


def all_categories(soup, category_list, relative_home_url):
    """
    Extract all categories name
    :param soup: BeautifulSoup object
    :param category_list: existing list for completion
    :param relative_home_url:
    :return: category_list completed
    """
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
    """
Extract all book urls
    :param soup:BeautifulSoup object
    :param url_home_relatif:(str)
    :return:list with all links
    """
    list_all_links = []
    for h3 in soup.find_all("h3"):
        a = h3.find("a")
        relatif_link = str(a["href"])
        absolute_link = url_home_relatif + str("catalogue/") + relatif_link.replace('../', "")
        list_all_links.append(absolute_link)

    return list_all_links


def next_link(soup):
    """
    Find the next page link
    :param soup: BeautifulSoup object
    :return: None or the link of next page
    """
    return soup.find("a", string="next")
