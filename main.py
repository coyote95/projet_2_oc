from bs4 import BeautifulSoup
import os
import extract
import transform
import load


url_home = "http://books.toscrape.com/index.html"
url_home_relatif = transform.url_relatif(url_home)

# category between 0 and 51
first_category = 0
last_category =51


def main():
    books_data_list = []
    list_all_urls_page = []
    categories_list = []

    html_home = extract.extract_html(url_home)
    soup_home = BeautifulSoup(html_home, "html.parser")

    # ***************************        Retrieve Categories     **********************

    categories_list = extract.all_categories(soup_home, categories_list, url_home_relatif)

    for category in categories_list[first_category:last_category]:
        books_data_list.clear()
        list_all_urls_page.clear()
        print(category.get("name"))
        name_csv = category.get("name")
        url_current = category.get("url")

        while True:
            html_current = extract.extract_html(url_current)
            soup_current = BeautifulSoup(html_current, "html.parser")

            if extract.next_link(soup_current):
                list_all_urls_page += extract.all_book_urls(soup_current, url_home_relatif)
                url_current = transform.url_relatif(url_current) + extract.next_link(soup_current)["href"]
                print(url_current)
            else:
                list_all_urls_page += extract.all_book_urls(soup_current, url_home_relatif)
                print(url_current)
                break

        for page in list_all_urls_page:
            print(f"Sracpping page: {page}")
            html_page = extract.extract_html(page)
            soup_page = BeautifulSoup(html_page, "html.parser")
            books_data_list.append(transform.dict_data_books(soup_page, page, url_home_relatif))
            load.csv_file(books_data_list, name_csv)

        # *******************************     Save images    *********************

        if not os.path.exists(f"images/{name_csv}"):
            os.makedirs(f"images/{name_csv}")

        i = 0
        for book in books_data_list:
            i += 1
            url_img = book.get("img_url")
            print(f'link image download:{url_img}')
            name_livre = book.get("title")
            name_livre = transform.clean_name(name_livre)
            image_save_path = os.path.join(f"images/{name_csv}", f"{name_livre}.jpg")
            if not os.path.exists(image_save_path):
                load.download_image(url_img, image_save_path)
            else:
                print(i)
                image_save_path = os.path.join(f"images/{name_csv}", f"{name_livre}_{i}.jpg")
                load.download_image(url_img, image_save_path)

    return


if __name__ == '__main__':
    main()
