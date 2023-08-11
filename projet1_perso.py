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
    return soup.title.string

def main():
    html_home=extract_data(URL_home)
    html_page_livre=extract_data(URL_page_livre)
    soup_home=BeautifulSoup(html_home,"html.parser")
    soup_livre = BeautifulSoup(html_page_livre, "html.parser")
    print(title(soup_home))
    save_page_html(soup_home,"page_home_html.txt")
    save_page_html(soup_livre, "page_livre.txt")

    return

main()