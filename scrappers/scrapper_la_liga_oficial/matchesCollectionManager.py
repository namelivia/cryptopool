from pymongo import MongoClient
from bson.objectid import ObjectId
from random import randint

class MatchesCollectionManager:

	def find_a_match(self, player1, player2, date):
		db = MongoClient('localhost',3001).meteor
		matchesCollection = db.matches
		return matchesCollection.find_one({
			"player1" : ObjectId(player1),
			"player2" : ObjectId(player2),
			"date" : date
		})

	def insert_a_new_match(self, newMatch):
		db = MongoClient('localhost',3001).meteor
		matchesCollection = db.matches
		return matchesCollection.insert(newMatch)

	def update_an_existing_match(self, match):
		db = MongoClient('localhost',3001).meteor
		matchesCollection = db.matches
		return matchesCollection.update({'_id' : match['_id']}, {"$set" : match})

	def get_a_random_unplayed_match(self):
		query = {
			'status' : 0
		}
		db = MongoClient('localhost',3001).meteor
		matchesCollection = db.matches
		matchesCount = matchesCollection.find(query).count()
		if matchesCount == 0 :
			return None
		index = randint(0, matchesCount-1)
		return matchesCollection.find(query).limit(-1).skip(index).next()
