from gevent import sleep
import requests
from datetime import datetime as dt

while True:
	r = requests.get('http://allrecipes.com/recipes')
	print r.status_code
	sleep(0.01)
