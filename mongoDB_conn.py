
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from jsonfile import StringToJson
from dotenv import load_dotenv
import os
load_dotenv()
username = os.environ.get("MONGO_USERNAME")
password = os.environ.get("MONGO_PASSWORD")
uri = f"mongodb+srv://{username}:{password}@grocerylist.3xhw3ou.mongodb.net/?retryWrites=true&w=majority&appName=GroceryList"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

database = client["Grocery"]
collection = database["items_data"]

def InsertJson(json_data):
    collection.insert_one(json_data)
    
