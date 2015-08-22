from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Tracker(Base):

    __tablename__ = "trackers"
    id = Column(Integer, primary_key=True)
    last_url = Column(Text)

    def __init__(self, last_url):
        self.last_url = last_url
