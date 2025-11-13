import sys
from pathlib import Path
import time
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Test Code below
from cogs.helldivers2.hd2_data import test as hd2_data_test


def test():
    start = time.time()
    hd2_data_test()
    
    stop = time.time()
    
    print(f"Test took {stop - start} sec")

if __name__ == "__main__":
    test()