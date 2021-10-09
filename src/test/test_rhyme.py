
import unittest
from lib.Rhymes import Rhymes


class TetstRhymes(unittest.TestCase):
    
        def test_rhyme_augen_german(self):
            word = "augen"
            possible_words = ["taugen", "lauben", "rauben", "tauben", "hauben", "saugen", "laugen", "glauben", "klauben", "stauben", "trauben", "strauben", "auslaugen", "schrauben", "schnauben"]
            
            rhyme = Rhymes.reime(word)
            
            assert rhyme in possible_words
            assert rhyme != word
            
            
        def test_rhyme_urlaub_german(self):
            word = "urlaub"
            
            rhyme = Rhymes.reime(word)
            
            assert rhyme != word
            
        def test_rhyme_no_rhyme_german(self):
            # if the algorithm does not find anything, return None
            word = "NONONONONONONONONASDONAOSDNAOSDNAOSDNAODNAONAOSDNOASDNOASDN"
            
            rhyme = Rhymes.reime(word)
            
            assert rhyme == "kein Reim gefunden"
            
