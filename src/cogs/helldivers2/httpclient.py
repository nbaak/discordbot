import requests
from typing import Union


def get(endpoint:str, headers:Union[dict, None]=None):
    headers = headers or {}
    response = requests.get(endpoint, headers=headers)
    
    return response.json()
