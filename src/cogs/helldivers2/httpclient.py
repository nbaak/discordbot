import requests
from typing import Union, Tuple


def __get(endpoint:str, headers:Union[dict, None]=None, params:Union[dict, None]=None) -> Tuple[Union[dict, None], bool]:
    headers = headers or {}

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        return response.json(), response.ok

    except requests.exceptions.HTTPError as http_err:
        print(f"error on endpoint: {endpoint}")
        print(f"HTTP error: {http_err}")

    except Exception as e:
        print(f"error on endpoint: {endpoint}")
        print(e)

    return {}, False


get = __get


def test():
    url = "https://example.com"
    response = get(url)
    print(response) 


if __name__ == "__main__":
    test()
