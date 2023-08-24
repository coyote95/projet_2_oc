import extract

"""
    Module for data manipulation:       -url clean
                                        - file name clean
                                        - create dictionnary with data book info

"""


def url_relatif(url):
    """
    Removes last element in URL
    :param url: (str) url with ex /index.html
    :return: (str) url modified ex /
    """
    path_segement=url.split("/")
    new_path_segement=path_segement[:-1]
    new_url="/".join(new_path_segement)+"/"
    return new_url


def clean_name(file_title):
    """
    Cleans a file title and returns a valid name for file
    :param file_title: (str)
    :return: (str)
    """
    new_name = ""
    valid_chars = "-_.()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for c in file_title:
        if c in valid_chars:
            new_name += c
        else:
            new_name += "_"
    if len(new_name) > 30:
        new_name = new_name[:30]

    return new_name


def dict_data_books(soup, page, url_home_relatif):

    """
    Create dictionnary with data information
    :param soup: Beautiful soup object
    :param page: (str)  url of book
    :param url_home_relatif:
    :return: books_data_list:list of dict completed
    """
    td = extract.column_table(soup)
    book_info_dict = {
        "universal_product_code(upc)": td[0],
        "price_excluding_tax": td[2],
        "price_including_tax": td[3],
        "number_available": td[5],
        "review_rating": td[6],
        "title": soup.find('h1').string,
        "product_page_url": page,
        "product_description": extract.book_description(soup),
        "category": extract.book_category(soup),
        "img_url": extract.url_image(soup, url_home_relatif)
    }

    return book_info_dict
