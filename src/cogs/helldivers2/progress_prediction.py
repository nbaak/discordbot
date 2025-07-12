

from collections import deque
from typing import Union
import time


class ProgressPrediction:
    
    def __init__(self, sample: Union[int, None]=None, time_value: Union[int, None]=None, target_value: int=0, count_up: bool=False, queue_len: int=5):
        self.last_value = sample     
        self.target = target_value   
        self.last_time = time_value or int(time.time())
        self.deltas = deque(maxlen=queue_len)
        self.count_up = count_up
        
    def add_sample(self, sample: int, ts:int) -> Union[int, None]:
        if self.last_value is not None:
            if self.count_up:
                delta = sample - self.last_value
            else:
                delta = self.last_value - sample
            
            delta_time = ts - self.last_time
            
            if delta_time == 0: return None
            
            # Normalize the delta by the time difference
            self.deltas.append(delta / delta_time)
            
            return delta
        
        else:
            return None
        
    def mean(self):
        return sum(self.deltas) / len(self.deltas)
    
    def calculate_progress(self, sample: int, ts: int) -> Union[float, None]:
        """
        Calculate the progress given a new sample and timestamp.
        """
        self.add_sample(sample, ts)
        p_time = None
        
        if any(self.deltas):
            mean_delta = self.mean()  # trend
            # p_time = sample / mean_delta if mean_delta != 0 else None
            p_time = abs(self.target - sample) / mean_delta
        
        self.last_value = sample
        self.last_time = ts
        
        return p_time
    
    def calculate_progress_t(self, sample: int) -> Union[float, None]:
        """
        Calculate progress using the current timestamp.
        """
        ts = int(time.time())
        return self.calculate_progress(sample, ts)
    
    def __repr__(self):
        return f"{self.last_time} {self.last_value}"
        
    
def test_down():
    pp = ProgressPrediction(100)
    
    time.sleep(1)
    print(pp.calculate_progress_t(99))
    
    time.sleep(1)
    print(pp.calculate_progress_t(98))
    
    time.sleep(1)
    print(pp.calculate_progress_t(97))
    
    time.sleep(1)
    print("jump", pp.calculate_progress_t(94))
    
    time.sleep(1)
    print(pp.calculate_progress_t(93))
    
    time.sleep(1)
    print("back", pp.calculate_progress_t(95))
    
    time.sleep(1)
    print(pp.calculate_progress_t(93))
    print(pp.calculate_progress_t(93))
    
    print("down - done\n")
    
    
def test_up():
    pp = ProgressPrediction(0, target_value=10, count_up=True)

    time.sleep(1)
    print(pp.calculate_progress_t(1))
    
    time.sleep(1)
    print(pp.calculate_progress_t(2))
    
    time.sleep(1)
    print(pp.calculate_progress_t(3))
    
    time.sleep(1)
    print(pp.calculate_progress_t(4))
    
    time.sleep(2)
    print("back", pp.calculate_progress_t(8))
    
    time.sleep(1)
    print(pp.calculate_progress_t(6))
    
    time.sleep(1)
    print(pp.calculate_progress_t(7))
    
    time.sleep(1)
    print(pp.calculate_progress_t(10))
    
    print("up - done")

    
if __name__ == "__main__":
    test_down()
    test_up()
