import json
import requests
from collections import OrderedDict

url = "http://127.0.0.1:8000/signals-api/"
username = "Bob"
password = "Bob2019"

res = requests.get(url, auth=(username, password))
signals = res.json()
print(signals)
for i, entry in enumerate(signals):
    print(f"[{i}] {entry['core_description']}")
