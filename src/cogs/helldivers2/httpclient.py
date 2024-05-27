import requests
import json


def get(endpoint):
    data = requests.get(endpoint).text
    return json.loads(data)
