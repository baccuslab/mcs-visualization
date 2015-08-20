import socket
from threading import Thread
import numpy as np
from collections import deque
import time


class MCSClient(object):

    def __init__(self, client, name="Unnamed", role="Not specified", trigger=False):
        self.client = client
        self.name = name
        self.role = role
        self.trigger = trigger
        self.running = False

    def process(self, message):

        lines = message.decode('ascii').split("\n")
        mid = lines[0].upper()

        if mid == 'GET':
            key = lines[1]
            print('GET ' + key)

            if key in ('name', 'role', 'trigger', 'running'):
                return self.__dict__[key]
            elif key == 'data':
                n = int(lines[2])
                resp = np.vstack([self.data.popleft() for _ in range(n)]).tobytes()
                return int(len(resp)).to_bytes(4, 'little') + resp
            else:
                raise ValueError('Invalid key: ' + key)

        elif mid == 'SET':
            key = lines[1]
            if key in ('name', 'role', 'trigger'):
                self.__dict__[key] = lines[2]
                print('SET ' + key + ' ' + lines[2])
            else:
                raise ValueError('Invalid key: ' + key)

        elif mid == 'START':
            self.running = True;
            print('> Started data collection!')

        elif mid == 'INIT':
            Thread(target=self.collect, daemon=True).start()

        elif mid == 'KILL':
            self.running = False;
            print('> Stopped data collection!')

        else:
            raise ValueError('Unknown message: ' + mid)

        return None

    def collect(self):

        nChannels = 10
        freq = 0.1
        maxlen = 1e5

        phases = np.random.randn(nChannels) * 2 * np.pi
        self.data = deque([], int(maxlen))

        print('> Initialized data collection!')
        t0 = time.time()

        while True:
            if self.running:
                time.sleep(0.1)
                t = time.time() - t0
                self.data.append(np.sin(2 * np.pi * freq * t + phases).astype('f2'))

    def send(self, msg):

        # wrap = lambda msg: int(len(msg)).to_bytes(4, 'little') + msg

        if type(msg) is bytes:
            self.client.send(msg)

        else:
            self.client.send(str(msg).encode('ascii') + b'\n')

    def run(self):

        while True:

            req = self.client.recv(4)
            if not req:
                print("Connection closed!")
                break

            msg_length = int.from_bytes(req, byteorder='little')
            msg = self.client.recv(msg_length)
            print("--------------------")
            print("Message received.")
            res = self.process(msg)
            self.send(res)
            print("--------------------")


def mcsserver(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(host)
    sock.listen(5)
    print('=' * 40)
    print('Started server on {} at port {}'.format(*sock.getsockname()))
    print('=' * 40)

    while True:
        remote, addr = sock.accept()
        print("New connection from ", addr)
        client = MCSClient(remote)
        Thread(target=client.run, daemon=True).start()


if __name__ == '__main__':
    mcsserver(('', 12345))
