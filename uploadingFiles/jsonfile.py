import json

def GetTotal(Json):
    sum = 0
    for key in Json:
        if key != "date":#print all the keys that are not date, add the sum to find total
            sum = sum + Json[key]["sum"]
            print(Json[key]["sum"])
    
    return sum

def StringToJson(json_str: str):
    structured_json = json.loads(json_str)
    return structured_json

def SaveJSON(json_str: str):
    with open("sample.json", "a") as f:
        f.write(json_str)
        
# string = """{"spices_n_seasonings":{"count":9,"sum":2120},"food_staples":{"count":12,"sum":8392},"dryfruits_n_seeds":{"count":2,"sum":310},"oils_sauces_and_condiments":{"count":4,"sum":1155},"cleaning_and_household":{"count":6,"sum":2293},"personal_care":{"count":2,"sum":840}}"""

