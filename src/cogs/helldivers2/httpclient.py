import requests
from typing import Union


def get(endpoint:str, headers:Union[dict, None]=None, params:Union[dict, None]=None) -> Union[dict, None]:
    headers = headers or {}
    response = requests.get(endpoint, headers=headers, params=params)
    
    return response.json()
