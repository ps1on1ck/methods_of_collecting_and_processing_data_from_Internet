from pymongo import MongoClient


class MClient:
    def __init__(self, host, port, db_name, collection_name):
        client = MongoClient(host, port)
        db = client[db_name]
        self.collection = db[collection_name]

    def insert_many(self, items):
        return self.collection.insert_many(items)

    def insert_many_if_not_exist(self, items):
        for item in items:
            self.insert_if_not_exist('vacancy_id', item)

    def insert_if_not_exist(self, name, item):
        if not self.is_exist(name, item[name]):
            self.collection.insert_one(item)

    def is_exist(self, name, field):
        return bool(self.collection.find_one({name: {'$in': [field]}}))
