from pymongo import MongoClient, database
import subprocess
import threading
import pymongo
from datetime import datetime, timedelta, timezone
import time
import traceback

DBName = "test" #Use this to change which Database we're accessing
connectionURL = "mongodb+srv://vinjin000:EIGnqv7iswU8iQNo@cluster0.ak4lnaw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" #Put your database URL here
sensorTable = "Traffic Data" #Change this to the name of your sensor data table

def QueryToList(query):
	l = []

	for item in query:
		#extracvt the payload and uid from mongo
		device_asset_uid = item['payload']['device_asset_uid']
		#get the last key in the payload dict
		last_key = list(item['payload'].keys())[-1]
		#get the value of the item  based on the last key
		last_item = item['payload'][last_key]
		#append the values into as a matrix into l
		l.append([device_asset_uid, last_item])

	return l;

def QueryDatabase() -> []:
	global DBName
	global connectionURL
	global currentDBName
	global running
	global filterTime
	global sensorTable
	cluster = None
	client = None
	db = None
	
	try:
		cluster = connectionURL
		client = MongoClient(cluster)
		db = client[DBName]

		print("Database collections: ", db.list_collection_names())

		#We first ask the user which collection they'd like to draw from.
		sensorCollection = db[sensorTable]
		print("Table:", sensorCollection)

		timeNow = datetime.now(timezone.utc)
		print("\nCurrent UTC Time:", timeNow)

		#We convert the cursor that mongo gives us to a list for easier iteration.
		timeCutOff = timeNow - timedelta(minutes=5)

		queryNew = {
			"time":{"$gte":timeCutOff}
		}

		queryOld = {
			"time":{"$lte":timeCutOff}
		}

		projection ={
			"_id":0,
			"payload":1,
			"time" : 1
		}

		#for item in sensorTable.find(queryOld, projection): print(item)

		#query the database for old documents into the lists based off queryOld
		oldDocuments = QueryToList(sensorCollection.find(queryOld, projection))
		#query the database for new documents into the lists based off queryNew
		currentDocuments = QueryToList(sensorCollection.find(queryNew, projection))

		print("Current Docs:", len(currentDocuments))
		print("Old Docs:", len(oldDocuments))


		highways = {}

		for item in currentDocuments:
			#define a new projection for the metadata query
			newProjection = {'_id': 0, 'latitude': 1, 'longitude': 1, 'eventTypes':1}
			#intialize the metadata collection
			metaTable = db['Traffic Data_metadata']
			#query the metadata collection for the location information based on assetUid
			currLocation = metaTable.find_one({'assetUid': item[0]}, newProjection)

			if currLocation:
				#extract the highway name and format it
				hName = currLocation['eventTypes'][0][0]['boards'][0]['name']
				hName = hName.replace(' Device Board','')

				#print(highways)

				#extract the lat and long
				latitude = currLocation.get('latitude', 0)
				longitude = currLocation.get('longitude', 0)

				#if it already exits we update it, else add it to the highway dict
				if (latitude, longitude) in highways:
					highways[(latitude, longitude)] = [highways[(latitude, longitude)][0]+item[1], highways[(latitude, longitude)][1]+1, hName]
				else:
					highways[(latitude, longitude)] = [item[1],1,hName]

			currLocation = None


		sortList = []

		#sort the list
		for key in highways.keys():
			sortList.append([highways[key][0]/highways[key][1],highways[key][2]])

		#calculate the average value of each highway
		sortList = sorted(sortList, key=lambda item: item[0])

		output = []

		#append the highway and it's average for output
		for pair in sortList:
			output.append(pair[1])
			output.append(pair[0])
		
		return output

	except Exception as e:
		# print("Please make sure that this machine's IP has access to MongoDB.")
		print("Error:",e)
		traceback.print_exc()
		exit(0)

	finally:
		if client:
			client.close()
