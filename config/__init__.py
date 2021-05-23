import json


class Config:
    def __init__(self, path):
        self.path = path
        self.load()

    def load(self):
        with open(self.path) as file:
            self.__dict__ = json.load(file)
