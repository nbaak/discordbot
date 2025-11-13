import requests
from typing import Union


def get(endpoint:str, headers:Union[dict, None]=None, params:Union[dict, None]=None, timeout:float=10.0) -> Union[dict, None]:
    headers = headers or {}
    
    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=timeout)
        return response.json()
    
    except Exception as e:
        print(e)
        print(f"error on endpoin: {endpoint}")
        
        return None
