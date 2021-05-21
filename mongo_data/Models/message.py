from datetime import datetime
from mongo_data.document_base import Document, db
import re

word_list = ["nice", "nojs", "noice", "najs"]

class Message(Document):
    def __init__(self, message) -> None:
        self.collection = db[str(message.guild.id)]
        self._id = str(message.id)
        self.channel_id = str(message.channel.id)
        self.name = message.author.name
        self.matches = self.get_number_of_matches(message.content.lower())
        self.timestamp = datetime.now()

    def get_number_of_matches(self, message):
        return len(re.findall(f'({"|".join(word_list)})', message))

    def post(self):
        if self.matches:
            super().post()

    def delete(self):
        super().delete()

    def update(self):
        if self.matches:
            super().update()
            return
        self.delete()