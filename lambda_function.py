import json
import os
import requests
import csv
import boto3
import time
from arcgis.gis import GIS
s3client = boto3.client('s3')
ssmclient = boto3.client('ssm')
def lambda_handler(event, context):
	s3bucket = event['Records'][0]['s3']['bucket']['name']
	s3key = event['Records'][0]['s3']['object']['key']
	response = s3client.get_object( Bucket=str(s3bucket), Key=str(s3key))
	data = json.loads(response['Body'].read().decode('utf-8'))
	lst = []
	lst.append(str(data['DeviceId'])); lst.append(',');
	lst.append(str(data['ProductionKW'])); lst.append(',');
	lst.append(str(data['ConsumptionKW'])); lst.append(',');
	lst.append(str(data['Latitude'])); lst.append(',');
	lst.append(str(data['Longitude'])); lst.append(',');
	lst.append(str(data['Address']));
	csvdata = ''.join(lst)
	filename = '/tmp/smartmeters.csv'
	headers = 'DeviceId,ProductionKW,ConsumptionKW,Latitude,Longitude,Address'
	print(csvdata)
	with open(filename, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
		writer.writerow(headers.split(","))
		writer.writerow(csvdata.split(","))
	username = ssmclient.get_parameter(Name='ArcGISUsername')
	password = ssmclient.get_parameter(Name='ArcGISPassword')
	gis = GIS(str('https://www.arcgis.com'), str(username['Parameter']['Value']), str(password['Parameter']['Value']))
	my_content = gis.content.add({}, filename)
	time.sleep(2)
	item = gis.content.get(my_content.id)
	print(item.publish())