
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError, ConnectionFailure
# from jsonfile import StringToJson
from dotenv import load_dotenv
import os
load_dotenv()
username = os.environ.get("MONGO_USERNAME")
password = os.environ.get("MONGO_PASSWORD")
uri = f"mongodb+srv://{username}:{password}@grocerylist.3xhw3ou.mongodb.net/?retryWrites=true&w=majority&appName=GroceryList"

# Create a new client and connect to the server
try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Optional: Fail fast if connection is bad
    # client.admin.command('ping')
except ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
    raise

database = client["lists"]
# collection = database["items_data"]

def InsertJson(json_data, username):
    try:
        if(username == "Noman"):
            collection = database["baba"]
        else:
            collection = database["mustafa"]
        collection.insert_one(json_data)
        print("Data inserted successfully.")
    except PyMongoError as e:
        print(f"Error inserting data into MongoDB: {e}")
        raise e
    
