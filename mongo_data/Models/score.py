from mongo_data.document_base import Document, db


class Score(Document):
    def __init__(self, guild_id) -> None:
        self.collection = db[str(guild_id)]

    def get_by_date(self, start, end):
        return self.collection.find({'timestamp': {'$lt': end, '$gte': start}})

    def find(self, **kwargs):
        return [self(**item) for item in self.collection.find(kwargs)]

    def sort_score(self, scores):
        nice_count_view = [(v, k) for k, v in scores.items()]
        nice_count_view.sort(reverse=True)
        return nice_count_view

    def get(self, span=None):
        if not span:
            result = dict()
            for item in self.collection.find():
                try:
                    result[item["name"]] += item["matches"]
                except KeyError:
                    result[item["name"]] = item["matches"]
            return self.sort_score(result)
