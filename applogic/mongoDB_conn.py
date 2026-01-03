from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError, ConnectionFailure
from dotenv import load_dotenv
import os


class MongoDBConnector:
    def __init__(self):
        load_dotenv()
        self.username = os.environ.get("MONGO_USERNAME")
        self.password = os.environ.get("MONGO_PASSWORD")
        self.uri = f"mongodb+srv://{self.username}:{self.password}@grocerylist.3xhw3ou.mongodb.net/?retryWrites=true&w=majority&appName=GroceryList"
        self.client = None
        self.database = None
        self.authDatabase = None
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
    
    def connectToAuthDatabase(self):
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            self.authDatabase = self.client["authentication"]
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB Auth Database: {e}")
            raise
            

    def insert_json(self, json_data, username):
        try:
            collection = self._GetCollection(username)
            collection.insert_one(json_data)
            print("Data inserted successfully.")
        except PyMongoError as e:
            print(f"Error inserting data into MongoDB: {e}")
            raise e

    def _GetCollection(self, username):
        if(username == "Noman"):
            collection = self.database["baba"]
        else:
            collection = self.database["mustafa"]
        return collection

    def fetch_collection(self, username):
        collection = self._GetCollection(username)
        return collection
    
    def get_json_from_collection(self, collection):
        json = collection.find()
        print(json)
        return json
    
    def get_user(self, username):
        collection = self.authDatabase["username_passwords"]
        users = collection.find({"username": username})
        #need to get users from the database for authentication
        return users
        