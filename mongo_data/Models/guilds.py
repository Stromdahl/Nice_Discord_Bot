from datetime import datetime
from mongo_data.document_base import Document
from pymongo import collection



class Guild(Document):
    def __init__(self, collection) -> None:
        super().__init__(collection)

    def post(self, name, amount):
        self.save(name=name, amount=amount, timestamp=datetime.now())

    def get_user_amount(self, user):
        return [i["amount"] for i in self.collection.find({"name": user}, {"amount":1})]

    def get_total(self):
        result = dict()
        for item in self.collection.find():
            try:
                result[item["name"]] += item["amount"]
            except KeyError:
                result[item["name"]] = item["amount"]
        return result