from groq import Groq
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import time

# load_dotenv()
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

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


def ClassifyData(data):
    CategorizedData = client.chat.completions.create(
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
                "role":"user", "content": f"""Classify this list: {data}"""
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
    ClassifiedData = CategorizedData.choices[0].message.content
    
    return ClassifiedData

# list = """[{'Product': '| Arfa Chat Masala 100 GM', 'Qty': '2.00', 'Price': '80', 'Total': '180'}, {'Product': 'Arfa Corriander Powder 200 GM', 'Qty': '1.00', 'Price': '140', 'Total': '140'}, {'Product': 'Arfa Corriander Whole 100 GM', 'Qty': '1.00', 'Price': '70', 'Total': '70'}, {'Product': 'Arfa Fresh Plum Irani 200 GM', 'Qty': '1.00', 'Price': '210', 'Total': '210'}, {'Product': 'Arfa Green Cardmom 25 GM', 'Qty': '1.00', 'Price': '350', 'Total': '350'}, {'Product': 'Arfa Pomegranate Seeds 100 GM', 'Qty': '1.00', 'Price': '100', 'Total': '100'}, {'Product': 'Arfa Red Chilli Cutter Kunri 200 GM', 'Qty': '1.00', 'Price': '190', 'Total': '190'}, {'Product': 'Arfa Red Chilli Powder Kunri 200 GM', 'Qty': '1.00', 'Price': '240', 'Total': '240'}, {'Product': 'Arfa Steam Kalnaat Rice 1 KG', 'Qty': '5.00', 'Price': '385', 'Total': '1,925'}, {'Product': 'Aspine Washing Powder Original 1 KG', 'Qty': '2.00', 'Price': '440', 'Total': '880'}, {'Product': 'Bake Parlor Spaghetti 500 GM', 'Qty': '2.00', 'Price': '220', 'Total': '440'}, {'Product': 'Bake Parlor Twisted Macroni 400 GM', 'Qty': '2.00', 'Price': '165', 'Total': '330'}, {'Product': 'Bread Shop Plain Bread Large', 'Qty': '1.00', 'Price': '210', 'Total': '210'}, {'Product': 'Butterfly Value Pack 16 PCS', 'Qty': '2.00', 'Price': '599', 'Total': '1,198'}, {'Product': 'Diplitt Sauce Chilli Garlic 400 GM', 'Qty': '1.00', 'Price': '225', 'Total': '225'}, {'Product': 'English Tooth Paste 140 GM', 'Qty': '2.00', 'Price': '220', 'Total': '440'}, {'Product': 'Italla Pomace Olive Oil TIN 100 ML', 'Qty': '1.00', 'Price': '510', 'Total': '510'}, {'Product': 'Kitcy Cocoa Powder 200 GM', 'Qty': '1.00', 'Price': '590', 'Total': '590'}, {'Product': 'Kitcy Cooking Chocolate Dark 500G', 'Qty': '1.00', 'Price': '650', 'Total': '650'}, {'Product': 'Kitcy Cooking Chocolate Milk 500 GM', 'Qty': '1.00', 'Price': '645', 'Total': '645'}, {'Product': 'Kiwi Sc Lemon 500 ML', 'Qty': '1.00', 'Price': '380', 'Total': '380'}, {'Product': 'National Mango Jam 200 GM', 'Qty': '1.00', 'Price': '210', 'Total': '210'}, {'Product': 'PCC Maida 1 KG', 'Qty': '2.00', 'Price': '125', 'Total': '250'}, {'Product': 'PCC Sugar 1 KG', 'Qty': '2.00', 'Price': '177', 'Total': '354'}, {'Product': 'Rose Petal Tulip Tissue Roll 10 Pacsk 8+2', 'Qty': '1.00', 'Price': '720', 'Total': '720'}, {'Product': 'Safon Dishwash Bar 2Long Bars 540 GM', 'Qty': '1.00', 'Price': '125', 'Total': '125'}, {'Product': 'Safon Dishwashing Powder 450 GM', 'Qty': '1.00', 'Price': '78', 'Total': '78'}, {'Product': 'Shan Himalayan Pink Salt 800 GM', 'Qty': '1.00', 'Price': '95', 'Total': '95'}, {'Product': 'Shan Korma Masala 50 GM X 2', 'Qty': '1.00', 'Price': '285', 'Total': '285'}, {'Product': 'Shan Special Bombay Biryani D-P', 'Qty': '2.00', 'Price': '285', 'Total': '570'}, {'Product': 'Shangrila Lemon Juice 275 ML', 'Qty': '1.00', 'Price': '210', 'Total': '210'}, {'Product': 'Shopping Bags', 'Qty': '1.00', 'Price': '70', 'Total': '70'}, {'Product': 'Sunridge Cornflour Chakki Atta 5 KG', 'Qty': '1.00', 'Price': '1,420', 'Total': '1,420'}, {'Product': 'Sweep Toilet Cleaner 500 ML', 'Qty': '2.00', 'Price': '210', 'Total': '420'}, {'Product': 'Vital Soap Gel Refilling Bundle Pack X140 GM', 'Qty': '1.00', 'Price': '400', 'Total': '400'}]"""
# data = ClassifyData(list)
# print(data)
# extract llm response
