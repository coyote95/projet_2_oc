import extract

"""
    Module for data manipulation:       -url clean
                                        - file name clean
                                        -english digit
                                        -delete symbol £
                                        -find digits
                                        - create dictionnary with data book info

"""


def url_relatif(url):
    """
    Removes last element in URL
    :param url: (str) url with ex /index.html
    :return: (str) url modified ex /
    """
    path_segement = url.split("/")
    new_path_segement = path_segement[:-1]
    new_url = "/".join(new_path_segement) + "/"
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


def english_digit(number):
    """
    Wirte number wit digits
    :param number(str)
    :return: number (str) "digit/5"
    """
    match number:
        case "One":
            number = "1/5"
        case "Two":
            number = "2/5"
        case "Three":
            number = "3/5"
        case "Four":
            number = "4/5"
        case "Five":
            number = "5/5"
    return number


def delete_symbol_pounds(price):
    """
    :param price: (str)
    :return: price (str)
    """
    return price.replace("£", "")


def find_digits(sentence):
    """

    :param sentence: str
    :return: sentence: (str) with only number
    """
    digits = ""
    for character in sentence:
        if character.isdigit():
            digits += character
    return digits


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
        "price_excluding_tax_£": delete_symbol_pounds(td[2]),
        "price_including_tax_£": delete_symbol_pounds(td[3]),
        "number_available": find_digits(td[5]),
        "review_rating": english_digit(extract.review_rating(soup)),
        "title": soup.find('h1').string,
        "product_page_url": page,
        "product_description": extract.book_description(soup),
        "category": extract.book_category(soup),
        "img_url": extract.url_image(soup, url_home_relatif)
    }

    return book_info_dict
