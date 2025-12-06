from google import genai
from google.genai import types
import dotenv
import streamlit as st
dotenv.load_dotenv()
import re
name = "WhatsApp Image 2025-09-30 at 7.36.54 PM.jpeg"
client = genai.Client()

def ExtractFromImage(name):
    with open(f'{name}', 'rb') as f:
      image_bytes = f.read()
    response = client.models.generate_content(
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
    st.subheader("Extracting Using AI")
    st.write(response.text)
    return response.text

def CleanResponse(text):
   pattern = r"\|\s*(.*?)\s*\|\s*([\d.]*)\s*\|\s*([\d,]*)\s*\|\s*([\d,.]*)\s*\|"

   matches = re.findall(pattern, text)
   
   # Clean results
   items = []
   for product, qty, price, total in matches:
       items.append({
           "Product": product.strip(),
           "Qty": qty.strip() if qty else None,
           "Price": price.strip() if price else None,
           "Total": total.strip() if total else None,
       })

   return items

 



def extract(name):
   data = ExtractFromImage(name)
   cleaned = CleanResponse(data)
   return cleaned
