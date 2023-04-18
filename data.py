from .downloader import downloader
from .parser import parser
import os.path
import json


def check(string):
    if os.path.exists(str(string)):
        return json.load(open(string))
    return string


def update(dict, path=""):
    dict = check(dict)

    if "main_page" not in dict and "day" not in dict:
        return dict

    for key in dict:
        for i, post in enumerate(dict[key]):
            d = downloader(url=post["link"], mode="get")
            d.save(path + "t.html")

            p = parser().parse_article(path + "t.html")
            for j in p.keys():
                dict[key][i][j] = p[j]

    os.remove(path + "t.html")
    return dict
