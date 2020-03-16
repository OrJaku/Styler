from bs4 import BeautifulSoup
import json
import requests
from PIL import Image
import urllib.request
import os

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
url = ''
with open('links.json') as f:
    data = json.load(f)
    for u in data:
        try:
            u = u['res_tshirts']
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

# for link in links:
#     try:
#         category = str(link).split("/")[-5]
#     except IndexError:
#         category = None
#     print(category)


i = 0
color_list = []
for link in links[1:]:
    i += 1
    product = str(link).split('"', 4)
    labels = product[1]
    label = str(labels).split('-', 4)

    try:
        product_color = label[2]
        product_color = str(product_color.strip())
        # print(product_color)
        if product_color is 'czarny':
            product_color = 'black'
        elif product_color == 'granatowy':
            product_color = 'navy'
        elif product_color == 'biały' or product_color == 'kość słoniowa':
            product_color = 'white'
        elif product_color == 'turkusowy':
            product_color = 'cyan'
        elif product_color == "brązowy":
            product_color = 'brown'
        elif product_color == "szary":
            product_color = 'gray'
        elif product_color == "niebieski":
            product_color = 'blue'
        elif product_color == "różowy":
            product_color = 'pink'
        elif product_color == "zielony":
            product_color = 'green'
        elif product_color == "beżowy":
            product_color = 'beige'
        elif product_color == "pomarańczowy":
            product_color = 'orange'
        elif product_color == "czerwony":
            product_color = 'red'
        elif product_color == "żółty":
            product_color = 'yellow'
        else:
            product_color = "other"
    except IndexError:
        product_color = "ColNaN"
    try:
        product_id_1 = label[3]
    except IndexError:
        product_id_1 = "IdNaN"
    try:
        product_id_2 = label[4]
    except IndexError:
        product_id_2 = "IdNaN"
    download_links = product[3]
    color_list.append(product_color)
    # print(product_color)
    try:
        img = Image.open(urllib.request.urlopen(download_links))
    except ValueError:
        img = None
    img_name = "".join([tag, "_", category, "_", product_id_1, product_id_2, "_", product_color, ".jpg"])
    try:
        path_image = "/".join([basedir, "download", img_name])
        img.save(path_image)
    except FileNotFoundError:
        print("Files problem")
    print(f"Downloading {i}/{len(links)}")
print(i)