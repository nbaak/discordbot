
import wikipedia
import random


class WikipediaWrapper:

    @staticmethod
    def search(topic):
        try:
            wikis = wikipedia.search(topic)

            num_wikis = len(wikis)

            # get ONE of them
            wiki = random.choice(wikis)
            summary = wikipedia.summary(wiki, sentences=3)
            page = wikipedia.page(wiki)

            content = f"{page.title}\n{page.summary.strip()}\n\n{page.url}"
            
        except Exception as e:
            content = "something went wrong :("

        return content
