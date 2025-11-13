import requests
from typing import Union


def get(endpoint:str, headers:Union[dict, None]=None, params:Union[dict, None]=None, timeout:float=10.0) -> Union[dict, None]:
    headers = headers or {}
    response = requests.get(endpoint, headers=headers, params=params, timeout=timeout)
    
    return response.json()
