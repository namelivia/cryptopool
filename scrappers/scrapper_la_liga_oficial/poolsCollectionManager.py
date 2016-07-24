from pymongo import MongoClient
from bson.objectid import ObjectId

class PoolsCollectionManager:

	def find_pools_by_match_id(self, matchId):
		db = MongoClient('localhost',3001).meteor
		poolsCollection = db.pools
		return poolsCollection.find({
			"match_id" : ObjectId(matchId),
		})

	def update_an_existing_pool(self, pool):
		db = MongoClient('localhost',3001).meteor
		poolsCollection = db.pools
		return poolsCollection.update({'_id' : pool['_id']}, {"$set" : pool})
