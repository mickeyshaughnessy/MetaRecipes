# This server runs the backend recipe service
# It has an API - see below
import sys
from flask import Flask
from flask import request, jsonify
from flask.ext.cors import CORS
from json import loads, dumps
import redis
from metarecipe import make_meta

from os.path import abspath
up = '/'.join(abspath(".").split('/')[:-1])
sys.path.append(up)
from config import *

redis = redis.StrictRedis(host=redis_hostname)

def get_all_recipes():
    keys = redis.keys('*recipe*')
    return [redis.get(key) for key in keys]

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/recipes/', methods=['GET'], defaults={'path':''})
@app.route('/recipes/<path:path>')
def recipes(path):
    if not path:
        data = get_all_recipes()
    else:
        data = redis.get(path)
    resp = {
            'message':'Have a nice day',
            'data':data
            }
    return jsonify(**resp)

@app.route('/metasearch/', methods=['GET'])
def metasearch():
    qstring = request.args.get('qstring')
    data = make_meta(qstring)
    resp = {
            'message':'Have a nice day with this recipe',
            'data':data
            }
    return jsonify(**resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)

