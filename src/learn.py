import nltk
nltk.data.path.append('/nltk')
from nltk.stem.snowball import GermanStemmer
#from nltk.stem.lancaster import LancasterStemmer # english stemmer

from lib.Tokenizer import Tokenizer
from ai.Model import Model
from ai.Bottler import Bottler
#from lib.FileGuard import FileGuard

import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import os

MODEL_FILE_NAME = 'model/chatbot.model'
TOKEN_FILE_NAME = 'pattern.tokens'
LABELS_FILE_NAME = 'labels.tokens'
INTENTS_FILE = 'intents.json'
EPOCHS = 2000

def get_json_data(json_file):
    with open(json_file) as file:
        data = json.load(file)
    
    return data
       
def learn():    
    tokenizer = Tokenizer()
    label_tokenizer = Tokenizer()
    
    try:
        tokenizer.load(TOKEN_FILE_NAME)
        label_tokenizer.load(LABELS_FILE_NAME)
        model = Model(MODEL_FILE_NAME, tokenizer.get_data_size(), label_tokenizer.get_data_size())
    
    except:
        stemmer = GermanStemmer()
        
        data = get_json_data(INTENTS_FILE)
        
        docs_x = []
        docs_y = []    
        
        for intent in data['intents']:        
            
            for pattern in intent['patterns']:
                pattern_tokens = tokenizer.classify(pattern.lower())
                docs_x.append(pattern_tokens)
                docs_y.append(label_tokenizer.classify(intent['tag']))
    
                
        training = []
        output = []
            
        for x, y in zip(docs_x, docs_y):
            training.append(tokenizer.tokens_to_1hot(x))
            output.append(label_tokenizer.tokens_to_1hot(y))
        
        
        # lits to np arrays
        training = np.array(training)
        output = np.array(output)
        
        # get a model
        model = Model(MODEL_FILE_NAME, len(training[0]), len(output[0]))
        
        # fit data to model
        model.get_model().fit(training, output, n_epoch=EPOCHS, batch_size=8, show_metric=False)
        
        # save it all
        model.save()
        tokenizer.save(TOKEN_FILE_NAME)
        label_tokenizer.save(LABELS_FILE_NAME)
        
        # check       
        for x,y in zip(docs_x, docs_y):
            print (f"x: {tokenizer.get_value(x)}, y: {label_tokenizer.get_value(y)}")
            
        print ("M", len(training[0]), len(output[0]))


def chat():
    from tensorflow.python.framework import ops
    ops.reset_default_graph()
    
    bottler = Bottler(MODEL_FILE_NAME, TOKEN_FILE_NAME, LABELS_FILE_NAME, INTENTS_FILE)
    
    recv = ""
    while True:
        recv = input("> ")
        if recv.lower() == 'quit':
            break
        
        result = bottler.answer(recv.lower(), 'Lauch')
        print(result)
            
if __name__ == '__main__':
    learn()
    chat()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            