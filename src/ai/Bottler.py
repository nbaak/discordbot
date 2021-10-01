
import json
import random

from lib.Tokenizer import Tokenizer
from ai.Model import Model

from tensorflow.python.framework import ops
ops.reset_default_graph()

def json_load(file):
    with open(file, 'r') as f:
        return json.load(f)


class Bottler:
    
    def __init__(self, model_path, word_tokens_path, label_tokens_path, intents):
        self.tokenizer = Tokenizer()
        self.label_tokenizer = Tokenizer()
        
        self.__load(model_path, word_tokens_path, label_tokens_path)
        self.intents = json_load(intents)
        
        
    def answer(self, text, user = None):
        prolly_tokens = self.tokenizer.sentence_to_1hot(text)
        # print(prolly_tokens)
        if max(prolly_tokens):
            result = self.model.predict_max([prolly_tokens])        
            label = self.label_tokenizer.get_value([result])[0]
            
            for intent in self.intents['intents']:
                if intent['tag'] == label:
                    if label == "greeting" and user:
                        if random.random() > .5:
                            return f"Hallo {user}!"
                        else:
                            return random.choice(intent['responses'])
                    else:
                        return random.choice(intent['responses'])
        
        return None
        
    
    
    def __load(self, model_path, word_tokens_path, label_tokens_path):
        self.tokenizer.load(word_tokens_path)
        self.label_tokenizer.load(label_tokens_path)
        self.model = Model(model_path, self.tokenizer.get_data_size(), self.label_tokenizer.get_data_size())
        self.model.load()