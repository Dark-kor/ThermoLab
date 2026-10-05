import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from daq.factory import create_source


def main():

    daq = create_source("simulator")

    daq.connect()

    frame = daq.acquire()

    print(frame)

    daq.disconnect()


if __name__ == "__main__":
    main()