import sys, os
sys.path.insert(0, '/var/www/MetaRecipes')
os.chdir('/var/www/MetaRecipes')

from metaserver import app as application
