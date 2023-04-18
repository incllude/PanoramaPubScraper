from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json


class parser:

    def __init__(self):

        self.result = {}
        self.url_static = "https://panorama.pub"

    def parse_article(self, source):

        attr = []
        texts = []
        months = ["янв.", "фев.", "мар.", "апр.", "май", "июн.", "июл.", "авг.", "сен.", "окт.", "ноя.", "дек."]
        self.result = {}

        with open(source) as f:
            soup = BeautifulSoup(f, "html.parser")
            self.result["image"] = soup.find("div", class_="w-full h-auto bg-cover bg-image").get("data-bg-image-jpeg")
            self.result["tittle"] = soup.find("h1").text.strip()
            self.result["rating"] = soup.find("span",
                                              class_="px-3 sm:px-4 py-1 text-md font-semibold bg-gray-100 "
                                                     "dark:bg-gray-500 text-gray-500 dark:text-gray-300").text.strip()
            self.result["rating"] = 0 if self.result["rating"] == '?' else int(self.result["rating"])
            for i in soup.find_all("div", class_="entry-contents"):
                texts.append(i.text)

            for i in soup.find("div", class_="flex flex-col gap-x-3 gap-y-1.5 flex-wrap sm:flex-row").find_all(
                    recursive=False):
                attr.append(i.text.strip())

        self.result["text"] = ' '.join([x.split() for x in texts][0])
        attr = [x.split() for x in attr]
        if attr[0][0] == "сегодня," or attr[0][0] == "вчера," or attr[0][0] == "позавчера,":
            date_string = ' '.join([datetime.now().strftime("%d %m %Y"), attr[0][-1]])
        else:
            date_string = ' '.join([attr[0][0], str(months.index(attr[0][1]) + 1), attr[0][2], attr[0][-1]])
        self.result["datetime"] = datetime.strptime(date_string, "%d %m %Y %H:%M")
        if attr[0][0] == "вчера,":
            self.result["datetime"] -= timedelta(days=1)
        elif attr[0][0] == "позавчера,":
            self.result["datetime"] -= timedelta(days=2)
        self.result["datetime"] = self.result["datetime"].strftime("%Y-%d-%m %H:%M")
        self.result["name"] = ' '.join(attr[1])
        self.result["tags"] = attr[2]

        return self.result

    def parse_main_page(self, source):

        self.result = {"main_page": []}

        with open(source) as f:
            soup = BeautifulSoup(f, "html.parser")
            tittles = []
            numbers = []
            images = []
            links = []
            for block in soup.find("ul", class_=["mt-4"]).find_all(recursive=False):
                texts = block.text.strip().split()
                links.append(self.url_static + block.find("a").get("href"))
                numbers_ = [int(x) for x in texts[-2:] if x.isdigit()]
                images.append(block.find("img").get("src"))
                if len(numbers_) == 1:
                    texts = texts[:-1]
                    numbers_.append(0)
                else:
                    texts = texts[:-2]
                numbers.append(numbers_)
                tittles.append(' '.join(texts))

        self.write(tittles, links, numbers, images)
        return self.result

    def parse_day(self, source):

        self.result = {"day": []}

        with open(source) as f:
            soup = BeautifulSoup(f, "html.parser")
            tittles = []
            numbers = []
            images = []
            links = []
            for block in soup.find("div", class_=["grid"]).find_all(recursive=False):
                links.append(self.url_static + block.get("href"))
                texts = block.text.strip().split()
                numbers_ = []
                if texts[0] == "Рейтинг:":
                    numbers_.append(int(texts[1]))
                    texts = texts[2:]
                else:
                    numbers_.append(0)
                if texts[1][:7] == "коммент":
                    numbers_.append(int(texts[0]))
                    texts = texts[2:]
                else:
                    numbers_.append(0)
                numbers.append(numbers_)
                images.append(block.find("img").get("src"))
                tittles.append(' '.join(texts))

        self.write(tittles, links, numbers, images)
        return self.result

    def write(self, tittles, links, numbers, images):
        for key in self.result:
            for i, text in enumerate(tittles):
                self.result[key].append({
                    "id": i,
                    "tittle": text,
                    "link": links[i],
                    "rating": numbers[i][0],
                    "comments": numbers[i][1],
                    "image": images[i]
                })

    def save(self, path):

        try:
            with open(path, 'w') as f:
                json.dump(self.result, f, indent=4)
        except FileNotFoundError:
            raise ValueError("Wrong way")
        except PermissionError:
            raise ValueError("Bad file's permissions")
