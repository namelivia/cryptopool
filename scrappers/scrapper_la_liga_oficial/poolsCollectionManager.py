from pymongo import MongoClient
from bson.objectid import ObjectId
from random import randint

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

	def get_a_random_open_pool_for_tokens(self, tokens):
		query = {
			'status_id' : 0,
			'amount' : { '$lte' : tokens},
		}
		db = MongoClient('localhost',3001).meteor
		poolsCollection = db.pools
		poolsCount = poolsCollection.find(query).count()
		if poolsCount == 0 :
			return None
		index = randint(0, poolsCount-1)
		return poolsCollection.find(query).limit(-1).skip(index).next()
