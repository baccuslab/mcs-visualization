from collections import deque
import numpy as np

BUFFER = deque

class DataBuffer(object):

    """Docstring for DataBuffer. """

    def __init__(self, nchannels=8, size=30, sampling_rate=20e3):
        """Initializes a DataBuffer """

        self.smplrate = sampling_rate
        self.nchannels = nchannels

        # initial_time = np.linspace(0, size, sampling_rate * size)
        # initial_data = np.sin(2*np.pi*initial_time*0.25).reshape(1,-1) + \
                       # np.random.randn(nchannels, sampling_rate) * 0.2

        # self.data = deque(list(initial_data), size * sampling_rate)
        # self.time = deque(list(initial_time), size * sampling_rate)

    def generate(self):
        """Generate a sample of new data"""

        np.random.randn(self.nchannels, )

    @property
    def dt(self):
        return 1 / self.smplrate

    def __len__(self):
        return len(self.data)
