import requests
import threading
from database import Database


class Main:
    def __init__(self):
        Database()
        self.start_urls = ['http://blog.scrapinghub.com']

    def parse(self):
        while True:
            t = threading.Thread(self.actions())
            t.daemon = True
            t.start()

    def actions(self):
        for url in self.start_urls:
            data = requests.get(url)
            print(data.content)


main = Main()
main.parse()
