from pymongo import MongoClient
from db_settings import *
from datetime import datetime

client = MongoClient(f'mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}')
db = client["discord_nice_bot"]


class Document:
    def __init__(self, collection) -> None:
        self.collection = db[collection]

    def get_date():
        return datetime.now().strftime("%Y-%m-%d")

    def save(self, **kwargs):
        return self.collection.insert_one(kwargs).inserted_id

    def update(self):
        return self.collection.update_one(self.__dict__)

    @classmethod
    def get_all(cls):
        return [cls(**item) for item in cls.collection.find({})]

    def get_by_date(self, start, end):
        print(start)
        print(end)
        pass

    def find(self, **kwargs):
        return [self(**item) for item in self.collection.find(kwargs)]
