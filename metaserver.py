# This server runs the backend recipe service
# It has an API - see below

from flask import Flask
from flask import request, jsonify
from json import loads, dumps
import redis
from metarecipe import make_meta

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
     
metaserver = Flask(__name__)

@metaserver.route('/recipes/', methods=['GET'], defaults={'path':''})
@metaserver.route('/recipes/<path:path>')
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

@metaserver.route('/metasearch/', methods=['POST'])
def metasearch():
    REQUEST = json.loads(request.data)
    data = make_meta(REQUEST['query'])
    resp = {
            'message':'Have a nice day with this recipe',
            'data':data
            }
    return jsonify(**resp)

if __name__ == '__main__':
    metaserver.run(host='0.0.0.0', port=5004, debug=True)





