
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from cogs.wikipedia.wikiwrapper import WikipediaWrapper


topics = ["Obama", "Linux", "Discord", "Star Citizen"]


print("\n\n+++++++++++++++++++++++++++++++++++++++++++++++\n\n")

for topic in topics:
    print(f"TEST: {topic}")
    print(WikipediaWrapper.search(topic))
    print("")

