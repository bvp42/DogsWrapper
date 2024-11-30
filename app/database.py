from pymongo import MongoClient
import os


class MongoDB:
    def __init__(self):
        self.client = MongoClient(os.environ["MONGO_URI"])
        self.db = self.client["dog_breeds"]
        self.collection = self.db["images"]

    def insert_one(self, document):
        self.collection.insert_one(document)

    def get_top_breeds(self):
        return self.collection.aggregate([
            {"$group": {"_id": "$breed", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ])

    def conection_test(self):
        return self.client.server_info()

    def close(self):
        self.client.close()


class MongoDBUsers:
    def __init__(self):
        self.client = MongoClient(os.environ["MONGO_URI"])
        self.db = self.client["dog_breeds"]
        self.collection = self.db["users"]

    def insert_one(self, document):
        self.collection.insert_one(document)

    def get_user(self, username):
        return self.collection.find_one({"username": username})

    def close(self):
        self.client.close()
