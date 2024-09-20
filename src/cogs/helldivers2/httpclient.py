import requests
import json
from typing import Union


def get(endpoint:str, headers:Union[dict, None]=None):
    headers = headers or {}
    response = requests.get(endpoint, headers=headers)
    # print(response.headers['x-ratelimit-limit'])
    json_data = json.loads(response.text)
    return json_data
