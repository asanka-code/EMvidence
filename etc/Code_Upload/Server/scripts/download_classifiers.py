import json
import requests
from collections import OrderedDict

url = "http://127.0.0.1:8000/classifiers-api/"
username = "Bob"
password = "Bob2019"

res = requests.get(url, auth=(username, password))
print(res)
classifiers = res.json()
print(classifiers)
for i, entry in enumerate(classifiers):
    print(f"[{i}] {entry['name']}")
