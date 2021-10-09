
import wikipedia

from lib.Wikipedia import WikipediaWrapper
import random


topics = ["Obama", "Linux", "Discord", "Star Citizen"]


print("\n\n+++++++++++++++++++++++++++++++++++++++++++++++\n\n")

for topic in topics:
    print(f"TEST: {topic}")
    print(WikipediaWrapper.search(topic))
    print("")

