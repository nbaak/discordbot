import requests
from typing import Union


def get(endpoint:str, headers:Union[dict, None]=None, params:Union[dict, None]=None) -> Union[dict, None]:
    headers = headers or {}
    
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        return response.json()
    
    except Exception as e:
        print(f"error on endpoint: {endpoint}")
        print(e)
        
        return None
