from collections import defaultdict
import re
from mongo_data.document_base import Document, db


class Score(Document):
    def __init__(self, guild_id) -> None:
        self.collection = db[str(guild_id)]

   

    def find(self, **kwargs):
        return [self(**item) for item in self.collection.find(kwargs)]

    def reduce(self, scores):
        result = defaultdict(int)
        for item in scores:
            result[item["name"]] += item["matches"]
        return [(v, k) for k, v in result.items()]

    def get(self):
        scores = self.reduce(self.collection.find())
        scores.sort(reverse=True)
        return scores

    def get_by_date(self, start, end):
        scores = self.collection.find({'timestamp': {'$lt': end, '$gte': start}})
        scores = self.reduce(scores)
        scores.sort(reverse=True)
        return scores
