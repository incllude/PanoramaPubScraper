import requests
from bs4 import BeautifulSoup


class downloader:

    def __init__(self, url, args=None, mode="get"):

        if mode == "get":
            just_req = requests.get(url=url, data=args)
            if just_req.status_code // 100 != 2:
                raise ValueError("Bad request")
            self.__raw = BeautifulSoup(just_req.content, "html.parser").prettify()
        elif mode == "post":
            just_req = requests.post(url=url, data=args)
            if just_req.status_code // 100 != 2:
                raise ValueError("Bad request")
        else:
            raise ValueError("Wrong start argument")

    def save(self, path):

        try:
            with open(path, "wb") as f:
                f.write(self.__raw.encode())
        except FileNotFoundError:
            raise ValueError("Wrong way")
        except PermissionError:
            raise ValueError("Bad file's permissions")

    def get_raw(self):
        return self.__raw

    raw = property(get_raw)
