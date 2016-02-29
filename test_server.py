import requests

resp = requests.get('http://localhost:5010/recipes/')
#resp = requests.get('http://localhost:5010/metasearch/')
resp = requests.get('http://localhost:5010/metasearch?qstring=applesauce')
print resp.text
