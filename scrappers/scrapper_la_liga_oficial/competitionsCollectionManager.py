from pymongo import MongoClient
from bson.objectid import ObjectId
from random import randint

class CompetitionsCollectionManager:

	def find_a_competition(self, code):
		db = MongoClient('localhost',3001).meteor
		competitionsCollection = db.competitions
		return competitionsCollection.find_one({
			"code" : code
		})

	def insert_a_new_competition(self, newCompetition):
		db = MongoClient('localhost',3001).meteor
		competitionsCollection = db.competitions
		return competitionsCollection.insert(newCompetition)

	def get_a_random_competition(self):
		db = MongoClient('localhost',3001).meteor
		competitionsCollection = db.competitions
		competitionsCount = competitionsCollection.find({}).count()
		if competitionsCount == 0 :
			return None
		index = randint(0, competitionsCount-1)
		return competitionsCollection.find({}).limit(-1).skip(index).next()
