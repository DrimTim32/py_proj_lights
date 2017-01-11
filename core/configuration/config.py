import json


class Config:
    def __init__(self):
        pass

    @staticmethod
    def from_config_file(file):
        f = open(file)
        data = json.load(f)
        #TODO
        return Config()
