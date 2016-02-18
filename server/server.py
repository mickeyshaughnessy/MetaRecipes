# This server runs the backend recipe service
# It has an API - see below

from flask import Flask
from flask import request, jsonify
from json import loads, dumps
import redis
from search import get_meta 

import sys
from os.path import abspath
up = '/'.join(abspath(".").split('/')[:-1])
sys.path.append(up)
from config import *

redis = redis.StrictRedis(host=redis_hostname)

def get_all_recipes():
    keys = redis.keys('*recipe*')
    return [redis.get(key) for key in keys]

def get_recipe(path):
    print(path)
    return redis.get(path)
     
app = Flask(__name__)

@app.route('/recipes/', methods=['GET'], defaults={'path':''})
@app.route('/recipes/<path:path>')
def recipes(path):
    if not path:
        data = get_all_recipes()
    else:
        data = get_recipe(path)
    resp = {
            'message':'Have a nice day',
            'data':data
            }
    return jsonify(**resp)

@app.route('/metasearch/', methods=['POST'])
def metasearch():
    REQUEST = json.loads(request.data)
    data = get_meta(REQUEST)
    resp = {
            'message':'Have a nice day with this recipe',
            'data':data
            }
    return jsonify(**resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)





