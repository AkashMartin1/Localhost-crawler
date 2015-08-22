from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from models.record import Record
from models.tracker import Tracker
import requests
import threading
import re
from blessings import Terminal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from database import Database
from models.domain import Domain


downloadable_files = ["mp4"]

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
            self.get_through_url()

    # @timeout(15)
    def get_through_url(self, url=None):
        if url is None:
            try:
                tracker = self.session.query(Tracker).one()
                url = tracker.last_url
            except NoResultFound, e:
                tracker = Tracker(last_url="https://en.wikipedia.org/wiki/Main_Page")
                self.session.add(tracker)
                self.session.commit()
                url = "https://en.wikipedia.org/wiki/Main_Page"
        else:
            tracker = self.session.query(Tracker).one()
            self.session.query(Tracker).filter(Tracker.id == tracker.id).update({'last_url': url})
            self.session.commit()

        response = requests.head(url)
        if int(response.headers["content-length"]) <= 2097152:
            data = requests.get(url)
            if self.session.query(Record).filter(Record.url == url).count() == 0:
                record = Record(url=url, text=data.content)
                self.session.add(record)
                self.session.commit()
            for data in re.findall(
                    r'(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?',
                    data.content):
                print(data)
                url = (data[0] + "://" + data[1] + data[2])
                print(Terminal().bold_red_on_bright_green("Scanning......." + url))
                try:
                    self.get_through_url(url)
                except Exception as e:
                    print(e)


main = Main()
main.parse()
