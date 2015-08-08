"""
Serve up data via a JSON API
"""

import time
import math
import random
from flask import Flask, json, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return "MCS Server!"

@app.route('/api/')
def api():
    t = time.time()
    ts = time.clock()
    y1 = math.sin(2*math.pi*ts*1) #+ 0.00*random.random()
    y2 = math.sin(2*math.pi*ts*5) #+ 0.00*random.random()
    data = [{'time': t, 'y': y1}, {'time': t, 'y': y2}]
    return json.jsonify(data=data)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
