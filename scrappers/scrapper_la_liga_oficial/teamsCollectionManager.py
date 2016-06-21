from pymongo import MongoClient
class TeamsCollectionManager:

	def find_a_team_by_name(self, name):
		db = MongoClient('localhost',3001).meteor
		teamsCollection = db.teams
		return teamsCollection.find_one({"name" : name})

	def insert_a_new_team(self, newTeam):
		db = MongoClient('localhost',3001).meteor
		teamsCollection = db.teams
		return teamsCollection.insert(newTeam)
