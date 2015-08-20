"""
Serve up data via a JSON API
"""

from socket import AF_INET, SOCK_STREAM, socket
import numpy as np
import matplotlib.pyplot as plt

wrap = lambda msg: int(len(msg)).to_bytes(4, 'little') + msg

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 12345))


sock.sendall(wrap(b'init\n'))
_ = sock.recv(1024)

sock.sendall(wrap(b'start\n'))
_ = sock.recv(1024)

N = 100
msg = 'get data {:d}'.format(N).replace(' ', '\n')
sock.sendall(wrap(msg.encode('ascii')))
length = int.from_bytes(sock.recv(4), 'little')
data = np.fromstring(sock.recv(length), 'f2').reshape(N, -1)
plt.plot(data)

# sock.close()
