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

    def post(self, **kwargs):
        kwargs["_id"] = str(kwargs["_id"])
        return self.collection.insert_one(kwargs).inserted_id

    def delete(self, _id):
        return self.collection.delete_one({"_id":str(_id)})

    def update(self, _id, **kwargs):
        return self.collection.update_one({"_id":str(_id)}, {"$set": kwargs})

    @classmethod
    def get_all(cls):
        return [cls(**item) for item in cls.collection.find({})]

    def get_by_date(self, start, end):
        return self.collection.find({'timestamp': {'$lt': end, '$gte': start}})

    def find(self, **kwargs):
        return [self(**item) for item in self.collection.find(kwargs)]
