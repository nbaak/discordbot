import pickle
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.snowball import GermanStemmer

class Tokenizer():
    
    def __init__(self, language="german", nltk_path="./nltk", stemming=False):
        nltk.data.path.append(nltk_path)
        nltk.download('punkt', download_dir=nltk_path)
        nltk.download('wordnet', download_dir=nltk_path)
        
        self.language = language
        self.stemming = stemming
        
        if language == 'german':
            self.stemmer = GermanStemmer()
        
        else:
            self.stemmer = LancasterStemmer()
            
        self.data = {}
        self.classify_index = -1
        
    
    def classify(self, text, lower=False):
        if lower:
            return self.__classify(text.lower())
        else:
            return self.__classify(text)
    
    def __classify(self, text, add=True):
        tokens = nltk.word_tokenize(text, language=self.language)
        classifiers = []
        
        for token in tokens:
            if token and token not in self.data and add:
                self.classify_index += 1
                self.data[token] = self.classify_index
        
            #print(f"classify index {self.classify_index}, key: {self.data[token]}, data: {token}")
            try:
                classifiers.append(self.data[token])
                #print (f"append: {self.data[token]}")
                #print (classifiers)
            except:
                pass
            
        return classifiers
    
    def get_value(self, classifiers = []):
        # reverse dict
        reversed_data = dict((v,k) for k, v in self.data.items())
        strings = []
        for classifier in classifiers:
            if classifier in reversed_data:
                strings.append(reversed_data[classifier])
            
        return strings
    
    def get_full_lenght_array(self):
        return [0 for _ in self.data]
    
    def get_data_size(self):
        return len(self.data)
    
    def tokens_to_1hot(self, tokens):
        onehot = self.get_full_lenght_array()
        
        for token in tokens:
            onehot[token] = 1
            
        return onehot
    
    def sentence_to_1hot(self, text):
        tokens = self.__classify(text, False)
        return self.tokens_to_1hot(tokens)
    
    def save(self, filename):
        d_store = {'data': self.data,
                   'index': self.classify_index}
        with open(filename, 'wb') as file:
            pickle.dump(d_store, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load(self, filename):
        with open(filename, 'rb') as file:
            d_store = pickle.load(file)
            self.data = d_store['data']
            self.classify_index = d_store['index']
            
            
            
            