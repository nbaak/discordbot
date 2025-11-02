import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Test Code below
from cogs.helldivers2.hd2_data import test


if __name__ == "__main__":
    test()