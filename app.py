from bs4 import BeautifulSoup
import json
import requests


url = ''
with open('links.json') as f:
    data = json.load(f)
    for u in data:
        try:
            u = u['reserved']
        except TypeError:
            u = None
        except KeyError:
            u = None
        if u:
            print(u)
            url = u


result = requests.get(url)

src = result.content
soup = BeautifulSoup(src, 'lxml')
links = soup.find_all("a")
for link in links:
    try:
        category = str(link).split("/")[-5]
    except IndexError:
        category = None
    print(category)

# i = 0
# for link in links:
#     i += 1
#     name = str(link).split('"', 2)[1]
#     print(name)
# print(i)