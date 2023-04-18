DEFAULT_URL = "https://panorama.pub"


def process(url=DEFAULT_URL, web_page_path="", data_path=""):
    url = url
    path = data_path

    d = downloader(url=url, mode="get")
    d.save(web_page_path + "panorama.html")

    p = parser()
    if url == DEFAULT_URL:
        r = p.parse_main_page(web_page_path + "panorama.html")
        path += "main_page.json"
    elif url[url.rfind('/') + 1:].replace('-', '').isdigit():
        r = p.parse_day(web_page_path + "panorama.html")
        path += "day.json"
    else:
        r = p.parse_article(web_page_path + "panorama.html")
        path += "article.json"

    p.save(path)
    return update(r)


if __name__ == "__main__":
    from downloader import downloader
    from parser import parser
    from data import update
else:
    from .downloader import downloader
    from .parser import parser
    from .data import update
