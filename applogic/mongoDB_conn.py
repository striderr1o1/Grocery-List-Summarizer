from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError, ConnectionFailure
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId


class MongoDBConnector:
    def __init__(self):
        load_dotenv()
        self.username = os.environ.get("MONGO_USERNAME")
        self.password = os.environ.get("MONGO_PASSWORD")
        self.uri = f"mongodb+srv://{self.username}:{self.password}@grocerylist.3xhw3ou.mongodb.net/?retryWrites=true&w=majority&appName=GroceryList"
        self.client = None
        self.client2 = None
        self.database = None
        self.authDatabase = None
        self._connect()
        self.username = ""

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
            self.client2 = MongoClient(self.uri, server_api=ServerApi('1'))
            self.authDatabase = self.client2["authentication"]
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
        check_exists = False
        collection_names = self.database.list_collection_names()
        for name in collection_names:
            if(name == username):
                check_exists = True
        if check_exists == True:
            collection = self.database[username]
            return collection
        try:
            self.database.create_collection(username, capped=True, size=10485760)
            print(f"Capped collection '{username}' created successfully.")
            collection = self.database[username]
            return collection
        except pymongo.errors.CollectionInvalid as e:
            print(f"Collection already exists or other error: {e}")

        

    def fetch_collection(self, username):
        self.username = username
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
        
    def InsertUser(self, username, hashed_password):
        collection = self.authDatabase["username_passwords"]
        collection.insert_one({
            "username": username,
            "password": hashed_password
        })
        return

    def getAuthenticationDatabase(self):
        self.connectToAuthDatabase()
        return self.authDatabase

    def get_detailedList_from_id(self, objectID):
        coll = self.fetch_collection(self.username)
        # 1. Convert string ID to ObjectId if needed
        if isinstance(objectID, str):
            try:
                objectID = ObjectId(objectID)
            except Exception:
                pass # If it fails, we try searching with the string as is

        # 2. Use find_one() instead of find()
        relevant_json = coll.find_one({"_id": objectID})
        
        # 3. Add safety check
        if relevant_json:
            return relevant_json.get("detailed_list")
        return "No details found."

        
