from datetime import datetime
from mongo_data.document_base import Document
from pymongo import collection



class Guild(Document):
    def __init__(self, collection) -> None:
        super().__init__(collection)

    def post(self, message_id, channel_id, name, amount):
        data = {
            "_id": message_id,
            "channel_id": channel_id,
            "name": name,
            "amount": amount,
            "timestamp": datetime.now()
        }
        super().post(**data)

    def delete(self, message_id):
        super().delete(message_id)

    def update(self, _id, amount):
        super().update(_id=_id, amount=amount)

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