from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError, ConnectionFailure
from dotenv import load_dotenv
import os
from pagess.existingdata import GetCollection

class MongoDBConnector:
    def __init__(self):
        load_dotenv()
        self.username = os.environ.get("MONGO_USERNAME")
        self.password = os.environ.get("MONGO_PASSWORD")
        self.uri = f"mongodb+srv://{self.username}:{self.password}@grocerylist.3xhw3ou.mongodb.net/?retryWrites=true&w=majority&appName=GroceryList"
        self.client = None
        self.database = None
        self._connect()

    def _connect(self):
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            # Optional: Fail fast if connection is bad
            # self.client.admin.command('ping')
            self.database = self.client["lists"]
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            raise

    def insert_json(self, json_data, username):
        try:
            collection = GetCollection(username)
            collection.insert_one(json_data)
            print("Data inserted successfully.")
        except PyMongoError as e:
            print(f"Error inserting data into MongoDB: {e}")
            raise e
