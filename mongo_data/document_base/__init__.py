from pymongo import MongoClient
from datetime import datetime
from config import Config

secrets = Config("config_files/secrets.json")

client = MongoClient(f'mongodb://{secrets.DB_USER}:{secrets.DB_PASSWORD}@{secrets.DB_HOST}:{secrets.DB_PORT}')
db = client[secrets.DB_NAME]

class Document:
    collection = None

    def get_date():
        return datetime.now().strftime("%Y-%m-%d")

    def post(self):
        data = self.__dict__.copy()
        data["collection"] = data["collection"].name
        return self.collection.insert_one(data).inserted_id

    def delete(self):
        return self.collection.delete_one({"_id": self._id})

    def update(self):
        data = self.__dict__.copy()
        data["collection"] = data["collection"].name
        return self.collection.update_one({"_id":self._id}, {"$set": data})

    @classmethod
    def get_all(cls):
        return [cls(**item) for item in cls.collection.find({})]

    def get_by_date(self, start, end):
        return self.collection.find({'timestamp': {'$lt': end, '$gte': start}})

    def find(self, **kwargs):
        return [self(**item) for item in self.collection.find(kwargs)]
