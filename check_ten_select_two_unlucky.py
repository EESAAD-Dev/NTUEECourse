import json, csv
import pandas as pd
import numpy as np

def read_json(filename):
    with open(filename, "r",encoding="utf-8") as f:
        json_object = json.loads(f.read())
    return json_object

result = pd.read_csv("result.csv") 
result1 = result.query("courseName == '十選二實驗'")
picked = result1["studentID"].to_numpy()
print("[Picked]\t%d" % len(set(picked)))

selections = read_json("selections.json")
selected_dict = {}
for selection in selections:
    studentID = selection["userID"]
    if selection["courseID"] == "Ten-Select-Two":
        
        selected_dict[studentID] = 1

selected = selected_dict.keys()
print("[Selected]\t%d" % len(set(selected)))

unlucky = list(set(selected) - set(picked))
print("[Unlucky]\t%d" % len(unlucky))
print(unlucky)
