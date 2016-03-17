import requests

#resp = requests.get('http://localhost:5010/recipes/')
#resp = requests.get('http://localhost:5010/metasearch/')
#resp = requests.get('http://localhost:5010/metasearch?qstring=applesauce')
resp = requests.get('http://ec2-54-200-146-86.us-west-2.compute.amazonaws.com/metasearch?qstring=applesauce')
print resp.text
