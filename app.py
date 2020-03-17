from bs4 import BeautifulSoup
import json
import requests
from PIL import Image
import urllib.request
import os

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)


def get_picture(link_url):
    url = ''
    with open('links.json') as f:
        data = json.load(f)
        for u in data:
            try:
                u = u[link_url]
                print("URL correct!")
            except TypeError:
                u = None
            except KeyError:
                u = None
            if u:
                print(u)
                url = u

    tag = str(url).split('/')[-1]
    print("Tag:", tag)
    category = str(url).split('/')[-4]
    print("Category:", category)
    result = requests.get(url)

    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    links = soup.find_all("img")
    i = 0
    color_list = []
    for link in links[1:]:
        i += 1
        product = str(link).split('"', 4)
        labels = product[1]
        label = str(labels).split(' - ', 5)
        try:
            product_color = label[1]
            product_color = str(product_color.strip())
        except IndexError:
            product_color = "ColNaN"
        if product_color == "other":
            print(f'Color: {label[1]}, Labels: {labels}')
        else:
            pass
        try:
            product_id_1 = label[2]
        except IndexError:
            product_id_1 = "IdNaN"
        try:
            product_id_2 = label[3]
        except IndexError:
            product_id_2 = "IdNaN"
        download_links = product[3]
        color_list.append(product_color)
        # print(product_color)
        try:
            img = Image.open(urllib.request.urlopen(download_links))
        except ValueError:
            img = None
        img_name = "".join([
            tag,
            "_",
            category,
            "_",
            product_color,
            "_", product_id_1,
            product_id_2, "_",
            product_color,
            ".jpg"
        ])
        try:
            path_image = "/".join([basedir, "download", img_name])
            img.save(path_image)
        except FileNotFoundError:
            print("Files problem")
        print(f"Downloading {i}/{len(links) -1 }")
    print(i)


get_picture('sweaters')
