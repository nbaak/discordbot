#!/usr/bin/env python3

import pickle
import argparse
from argparse import Namespace
from typing import Any
from pprint import pprint


def get_args() -> Namespace:
    parser = argparse.ArgumentParser(prog="Data Viwerer", description="Tool to have a quick look in a binary file object")
    parser.add_argument('-f', '--file', help='data file', type=str)
    
    return parser.parse_args()


def load_pickle(path:str) -> Any:
    with open(path, "rb") as handle:
        return pickle.load(handle)


def describe_object(obj:Any) -> None:
    print("Type:", type(obj))

    if hasattr(obj, "__len__"):
        try:
            print("Length:", len(obj))
        except TypeError:
            pass

    if isinstance(obj, dict):
        print("Keys:", list(obj.keys()))


def main() -> None:
    args = get_args()
    print(args)
    data = load_pickle(args.file)

    describe_object(data)
    print("\nData:\n")
    pprint(data)


if __name__ == "__main__":
    main()
