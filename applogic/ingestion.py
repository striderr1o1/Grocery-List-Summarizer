from google import genai
from google.genai import types
import dotenv
import streamlit as st
dotenv.load_dotenv()
import re
name = "WhatsApp Image 2025-09-30 at 7.36.54 PM.jpeg"
from groq import Groq
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import time
import json
from datetime import datetime
from applogic.mongoDB_conn import MongoDBConnector

load_dotenv()
clientGemini = genai.Client()
clientGroq = Groq(api_key=os.environ.get('GROQ_API_KEY'))

class Data(BaseModel):
    count: int
    sum: int

class Categories(BaseModel):
    spices_n_seasonings: Data
    food_staples: Data
    dryfruits_n_seeds: Data
    oils_sauces_and_condiments: Data
    cleaning_and_household: Data
    personal_care: Data
    vegetables_n_fruits: Data


class Ingestion:
    username = ""
    filename = ""
    extractedText = ""
    clean_list = ""
    classified_data = ""
    TotalSum = ""
    Json = {}
    DetailedJson = {} #added detailed json to database but it 
    # needs to be handled in other files also
    db = None
    def __init__(self, filename, username, dbase):
        self.filename = filename
        self.extractedText = ""
        self.clean_list = ""
        self.classified_data = ""
        self.Json = {}
        self.TotalSum = ""
        self.username = username
        self.db = dbase
        self.DetailedJson = {}
        return
    
    def _ExtractFromImage(self):
        with open(f'{self.filename}', 'rb') as f:
          image_bytes = f.read()
        response = clientGemini.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
              types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg',
              ),
              """Extract the information from this. Alway give information in the form of table. Dont give any other information other than the table.
              Dont extract any other information like contact, address and other irrelevant information. You are to extract only the list items."""
            ]
        )
        self.extractedText = response.text
        
    def _CleanResponse(self):
        pattern = r"\|\s*(.*?)\s*\|\s*([\d.]*)\s*\|\s*([\d,]*)\s*\|\s*([\d,.]*)\s*\|"
     
        matches = re.findall(pattern, self.extractedText)
        
        # Clean results
        items = []
        for product, qty, price, total in matches:
            items.append({
                "Product": product.strip(),
                "Qty": qty.strip() if qty else None,
                "Price": price.strip() if price else None,
                "Total": total.strip() if total else None,
            })
        self.clean_list = items
        
    def extract(self):
        self._ExtractFromImage()
        self._CleanResponse()
        self.convert_CleanList_to_Json()
        return self.clean_list, self.DetailedJson
    
    def ClassifyData(self):
        CategorizedData = clientGroq.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": """You are serving as a Grocery Item Classifier. You get a list of Grocery
                 items. You classify the items in the list in these four categories:
                 'Spices & Seasonings',
                 'Food Staples',
                 'Dry Fruits & Seeds',
                 'Oils, Sauces & Condiments',
                 'Cleaning & Household',
                 'Personal Care',
                 'Vegetables & Fruits'.
                 In the end, you return coumt of each class, and their total sum in a JSON format using the 
                 schema provided. Dont output anything other than the JSON, remember this.
                 
"""    
                },
                {
                    "role":"user", "content": f"""Classify this list: {self.clean_list}"""
                }
            ],
            response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "Categories",
                "schema": Categories.model_json_schema()
            }
        }
        )
        self.classified_data = CategorizedData.choices[0].message.content
        
        return self.classified_data
    
    
    def _GetTotal(self):
        sum = 0
        for key in self.Json:
            if key != "date":#print all the keys that are not date, add the sum to find total
                sum = sum + self.Json[key]["sum"]
                print(self.Json[key]["sum"])
        self.TotalSum = sum
        return self.TotalSum
    
    def _AddingDateTimeandTotalToJSON(self):
        self.Json["date"] = datetime.now().strftime("%Y-%m-%d")
        total_sum = self._GetTotal()
        self.Json["total"] = total_sum
    
    def StringToJson(self):
        self.Json = json.loads(self.classified_data)
       # self.DetailedJson = json.loads(self.clean_list)
       # self.Json["detailed_list"] = self.DetailedJson
        self._AddingDateTimeandTotalToJSON()
        return self.Json

    def save_to_db(self):
        if self.db is not None:
            self.db.insert_json(self.Json, self.username)
        else:
            print("None obj, save_to_db in ingestion.py")
    def convert_CleanList_to_Json(self):
        for i in range(0,len(self.clean_list)):
            self.DetailedJson[f"{i}"] = self.clean_list[i]
        
#convert clean list to dictionary and then to json, then send
# it to the database
