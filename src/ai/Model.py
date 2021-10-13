
import tflearn
import tensorflow as tf
import pickle
import numpy as np


class Model():   
    
    def __init__(self, filename, input_size=None, output_size=None):
        self.model = self.__create_network(input_size, output_size)
        
        self.filename = filename
        self.inputs = input_size
        self.outputs = output_size
    
    def __create_network(self, input_size, output_size):
        net = tflearn.input_data(shape=[None, input_size])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, output_size, activation="softmax")
        net = tflearn.regression(net)
        
        model = tflearn.DNN(net)
        return model
    
    def predict(self, data):
        return self.model.predict(data)
    
    def predict_max(self, data):
        probabilities_data = self.predict(data)[0]              # get probabilites for all possible outcomes
        probability_index = np.argmax(probabilities_data)       # returns the index with the highest probability
        probability_of_index = probabilities_data[probability_index]
        
        # debug..
        print(f"index: {probability_index}, probability: {probability_of_index}")
        print(probabilities_data)
        
        return probability_index, probability_of_index
    
    def get_model(self):
        return self.model
    
    def save(self):
        self.model.save(self.filename)
        
    def load(self):    
        self.model.load(self.filename)
        