import requests
from typing import Union, Tuple


def __get(endpoint:str, headers:Union[dict, None]=None, params:Union[dict, None]=None) -> Tuple[Union[dict, None], bool]:
    headers = headers or {}
    
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        return response.json(), response.ok
    
    except Exception as e:
        print(f"error on endpoint: {endpoint}")
        print(e)
        
    return None, False


get = __get


def test():
    url = "https://example.com"
    response = get(url)
    print(response) 


if __name__ == "__main__":
    test()
