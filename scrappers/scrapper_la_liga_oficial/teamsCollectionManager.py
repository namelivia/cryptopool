from pymongo import MongoClient
from random import randint

class TeamsCollectionManager:

	def find_a_team_by_name(self, name):
		db = MongoClient('localhost',3001).meteor
		teamsCollection = db.teams
		return teamsCollection.find_one({"name" : name})

	def insert_a_new_team(self, newTeam):
		db = MongoClient('localhost',3001).meteor
		teamsCollection = db.teams
		return teamsCollection.insert(newTeam)

	def get_a_random_team(self):
		db = MongoClient('localhost',3001).meteor
		teamsCollection = db.teams
		teamsCount = teamsCollection.find({}).count()
		if teamsCount == 0 :
			return None
		index = randint(0, teamsCount-1)
		return teamsCollection.find({}).limit(-1).skip(index).next()
