from pymongo import MongoClient
class TeamsCollectionManager:
	def __init__(self):
		db = MongoClient('localhost',3001).meteor
		self.teamsCollection = db.teams

	def find_a_team_by_name(self, name):
		return self.teamsCollection.find_one({"name" : name})

	def insert_a_new_team(self, newTeam):
		return self.teamsCollection.insert(newTeam)
