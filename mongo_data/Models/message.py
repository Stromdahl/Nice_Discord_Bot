from config import Config
from datetime import datetime
from mongo_data.document_base import Document, db
from mongo_data.Models.message_helpers import get_matches, get_score
import re

class Message(Document):
    def __init__(self, message) -> None:
        self.collection = db[str(message.guild.id)]
        self._id = str(message.id)
        self.channel_id = str(message.channel.id)
        self.name = message.author.name

        word_list = Config("config_files/config.json").WORD_LIST
        words = get_matches(message.content.lower(), word_list.keys())
        score = get_score(words, word_list)
        self.matches = score
        
        self.timestamp = datetime.now()

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