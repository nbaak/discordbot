from typing import Union, List
import pickle
import matplotlib.pyplot as plt 
from statistics import mean
import numpy as np


class QueueItem:
    
    def __init__(self, label:Union[int, str], item:Union[int, None]=None):
        self.label:Union[int, str] = label
        self.items:List = []
        if item:
            self.add(item)
        
    def add(self, item):
        self.items.append(item)
        

def find_in_list(list_of_items:List, label:int):
    if len(list_of_items) > 0:
        for item in list_of_items:
            if item.label == label:
                return item
    
    return None


class WalkingCounter:
    
    def __init__(self, max_len=24):
        self.max_len = max_len
        self._queue:List = []
    
    def append(self, label:Union[int, str], item=None): 
        q_item = find_in_list(self._queue, label)
        if q_item:
            q_item.add(item)
        else:
            q_item = QueueItem(label, item)
            self._queue.append(q_item)
        
        if len(self._queue) > self.max_len: 
            xitem = self._queue.pop(0)
            
        print(f"label: {label} {len(q_item.items)} {q_item.items}")
    
    def show(self):
        for qi in self._queue:
            print(qi.label, qi.items)
            
    def plot(self, filename="plot.jpg"):
        plt.cla()
        labels = [qi.label for qi in self._queue]
        mean_values = [mean(qi.items) for qi in self._queue]
        min_values = [min(qi.items) for qi in self._queue]
        max_values = [max(qi.items) for qi in self._queue]
        
        # plotting
        # plt.bar(labels, mean_values)
        fig, ax = plt.subplots(figsize=(3, 24))
        fig.set_size_inches(7, 5)
        
        # Set the width of the bars
        bar_width = 0.35

        # Calculate adjusted positions for Part 1 (a_values) and Part 2 (b_values)
        bar_positions = np.arange(len(labels))
        bar_positions_min = bar_positions - bar_width / 2
        bar_positions_max = bar_positions + bar_width / 2
        
        # Bar plots for Total, A, and B
        bar_mean = ax.bar(bar_positions, mean_values, bar_width, label='Mean', color='green')
        bar_min = ax.bar(bar_positions_min, min_values, bar_width, label='Min', color='blue')
        bar_max = ax.bar(bar_positions_max, max_values, bar_width, label='Max', color='red')
        
        # customize plot
        ax.set_title("Active Helldivers")
        ax.set_xlabel("Timestamps")
        ax.set_ylabel("Helldivers")
        ax.legend()
        ax.grid(True)
        
        
        plt.xticks(bar_positions, labels, rotation=90)
        # plt.show()
        plt.savefig(filename)
            
    def save(self, filename="counter.bin"):
        with open(filename, 'wb') as f:
            pickle.dump(self, f) 
    
    def load(self, filename="counter.bin"):
        try:
            with open(filename, 'rb') as f:
                obj = pickle.load(f)
                self.max_len = obj.max_len
                self._queue = obj._queue
        except FileNotFoundError:
            pass
        
        
def main():
    import random
    wc = WalkingCounter(max_len=24)
    # wc.load()
    for day in range(0, random.randint(1, 5)): 
        for hour in range(24):
            entries = random.randint(1, 5)
            # print(f"day: {day}, hour: {hour:02}, num of values: {entries}")
            ts = f"{day}-{hour:02}"
            for _ in range(1, entries + 1):
                wc.append(ts, random.randint(1,1000))
            wc.plot()
    
    wc.show()
    # wc.save()
    
    print(len(wc._queue))


if __name__ == "__main__":
    main()
