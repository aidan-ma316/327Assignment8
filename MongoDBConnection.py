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

		device_asset_uid = item['payload']['device_asset_uid']

		last_key = list(item['payload'].keys())[-1]

		last_item = item['payload'][last_key]

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

		oldDocuments = QueryToList(sensorCollection.find(queryOld, projection))

		currentDocuments = QueryToList(sensorCollection.find(queryNew, projection))

		print("Current Docs:", len(currentDocuments))
		print("Old Docs:", len(oldDocuments))


		highways = {}

		for item in currentDocuments:

			newProjection = {'_id': 0, 'latitude': 1, 'longitude': 1, 'eventTypes':1}

			metaTable = db['Traffic Data_metadata']

			currLocation = metaTable.find_one({'assetUid': item[0]}, newProjection)

			if currLocation:
				hName = currLocation['eventTypes'][0][0]['boards'][0]['name']
				hName = hName.replace(' Device Board','')

				#print(highways)

				latitude = currLocation.get('latitude', 0)
				longitude = currLocation.get('longitude', 0)

				if (latitude, longitude) in highways:
					highways[(latitude, longitude)] = [highways[(latitude, longitude)][0]+item[1], highways[(latitude, longitude)][1]+1, hName]
				else:
					highways[(latitude, longitude)] = [item[1],1,hName]

			currLocation = None


		sortList = []

		for key in highways.keys():
			sortList.append([highways[key][0]/highways[key][1],highways[key][2]])

		sortList = sorted(sortList, key=lambda item: item[0])

		output = []

		for pair in sortList:
			output.append(pair[1])
			output.append(pair[0])
		
		return output

	except Exception as e:
		# print("Please make sure that this machine's IP has access to MongoDB.")
		print("Error:",e)
		traceback.print_exc()
		exit(0)

# 	# finally:
# 	# 	if client:
# 	# 		client.close()
