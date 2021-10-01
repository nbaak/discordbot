import pronouncing
import random
import requests
import duden
from bs4 import BeautifulSoup as bs


class Rhymes():    
    
    @staticmethod 
    def rhyme(word):
        return Rhymes.rhyme_en(word)
    
    @staticmethod 
    def reime(word):
        return Rhymes.rhyme_de(word)
    
    @staticmethod
    def rhyme_en(word):
        try:
            return random.choice(pronouncing.rhymes(word))
        
        except Exception as e:
            print (f"Exception {e}")
            return "no Rhyme found :("
        
        
    @staticmethod
    def rhyme_de(word):
        url = f"https://www.was-reimt-sich-auf.de/{word}.html"
        
        req = requests.get(url)
        soup = bs(req.content, 'html.parser')
        
        elements = soup.find(class_='rhymes').find_all('li')
        
        rhymes = []
        for element in elements:
            try:
                if word != element['data-rhyme']:
                    rhymes.append(element['data-rhyme'])
            except:
                pass
            
        return random.choice(rhymes)
        

    @staticmethod 
    def syllables(word):
        return Rhymes.syllables_de(word)
    
    @staticmethod 
    def syllables_de(word):
        w = duden.get(word)
        try:
            return ' '.join(w.word_separation)
        except:
            return f"{word} ist kein bekanntes Wort oder es ist nicht richtig geschrieben. Groß-/Kleinschreibung sind wichtig!"
    
    
    
    



















