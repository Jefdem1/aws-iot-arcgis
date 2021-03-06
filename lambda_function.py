import json
import os
import requests
from arcgis.gis import GIS

def lambda_handler(event, context):
	print("ArcGIS Online Org account")
	gis = GIS(str(os.environ['url']), str(os.environ['username']), str(os.environ['password']))
	print("Logged in as " + str(gis.properties.user.username))
	return str(gis.properties.user.username)
