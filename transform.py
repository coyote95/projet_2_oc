import extract


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


def data_livres(soup, produits, page):
    td = extract.tableau_colonne(soup)
    dict_livre_info = {
        "universal_product_code(upc)": td[0],
        "price_excluding_tax": td[2],
        "price_including_tax": td[3],
        "number_available": td[5],
        "review_rating": td[6],
        "title": soup.find('h1').string,
        "product_page_url": page,
        "product_description": extract.description_livre(soup),
        "category": extract.categorie(soup),
        "img_url": extract.url_image(soup)
    }

    produits.append(dict_livre_info)

    return produits
