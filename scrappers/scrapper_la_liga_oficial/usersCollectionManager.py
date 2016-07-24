from pymongo import MongoClient
from bson.objectid import ObjectId

class UsersCollectionManager:

	def find_user_by_id(self, userId):
		db = MongoClient('localhost',3001).meteor
		usersCollection = db.users
		return usersCollection.find_one({
			"_id" : ObjectId(userId),
		})

	def update_an_existing_user(self, user):
		db = MongoClient('localhost',3001).meteor
		usersCollection = db.users
		return usersCollection.update({'_id' : user['_id']}, {"$set" : user})
