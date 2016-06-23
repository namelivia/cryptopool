from pymongo import MongoClient
from bson.objectid import ObjectId

class MatchesCollectionManager:
	def __init__(self):
		db = MongoClient('localhost',3001).meteor
		self.matchesCollection = db.matches

	def find_a_match(self, player1, player2, date):
		return self.matchesCollection.find_one({
			"player1" : ObjectId(player1),
			"player2" : ObjectId(player2),
			"date" : date
		})

	def insert_a_new_match(self, newMatch):
		return self.matchesCollection.insert(newMatch)

	def update_an_existing_match(self, match):
		return self.matchesCollection.update({'_id' : match['_id']}, {"$set" : match})
