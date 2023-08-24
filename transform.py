import extract


# Removes 'index.html' from a URL
def delete_url_index(url):
    return url.replace('index.html', '')


# Cleans a file title and returns a valid name for file
def clean_name(file_title):
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


def data_books(soup, products, page, url_home_relatif):
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

    products.append(book_info_dict)

    return products
