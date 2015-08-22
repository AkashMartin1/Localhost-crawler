from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Domain(Base):

    __tablename__ = "domains"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    def __init__(self, name):
        init_url = "https://en.wikipedia.org/wiki/Main_Page"
        self.name = name
