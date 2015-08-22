import requests
import threading
import re
from blessings import Terminal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from database import Database
from models.domain import Domain


class Main:
    def __init__(self):
        self.engine = Database().connect()
        self.start_urls = ['http://blog.scrapinghub.com']
        # Insert multiple data in this session, similarly you can delete
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        if self.session.query(Domain).count() == 0:
            domain = Domain(name="https://en.wikipedia.org/wiki/Main_Page")
            self.session.add(domain)
            try:
                self.session.commit()
            # You can catch exceptions with  SQLAlchemyError base class
            except SQLAlchemyError as e:
                self.session.rollback()
                print(str(e))

    def parse(self):
        while True:
            t = threading.Thread(self.actions())
            t.daemon = True
            t.start()

    def actions(self):
        for url in self.session.query(Domain).limit(10):
            self.get_through_url(url.name)

    def get_through_url(self, url):
        data = requests.get(url)
        for data in re.findall(
                r'(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?',
                data.content):
            print(data)
            url = (data[0] + "://" + data[1] + "/" + data[2])
            print(Terminal().bold_red_on_bright_green("Scanning......." + url))
            self.get_through_url(url)


main = Main()
main.parse()
