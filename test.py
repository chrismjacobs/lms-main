
import json

x = {}
with open('static/json_files/FRD1/sources.json', 'r') as rf:
    x = json.load(rf)

print(x)