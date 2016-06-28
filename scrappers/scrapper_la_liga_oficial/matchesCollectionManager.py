from pymongo import MongoClient
from bson.objectid import ObjectId
from reportsGenerator import ReportsGenerator

class MatchesCollectionManager:
	def __init__(self):
		self.reportsGenerator = ReportsGenerator()

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
		self.reportsGenerator.generate_insert_match_record(newMatch);
		return matchesCollection.insert(newMatch)

	def update_an_existing_match(self, match):
		db = MongoClient('localhost',3001).meteor
		matchesCollection = db.matches
		self.reportsGenerator.generate_updated_match_record(match);
		return matchesCollection.update({'_id' : match['_id']}, {"$set" : match})
