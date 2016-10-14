from pymongo import MongoClient
from random import randint

class UsersCollectionManager:

	def find_user_by_id(self, userId):
		db = MongoClient('localhost',3001).meteor
		usersCollection = db.users
		return usersCollection.find_one({
			"_id" : userId
		})

	def find_user_by_username(self, username):
		db = MongoClient('localhost',3001).meteor
		usersCollection = db.users
		return usersCollection.find_one({
			"username" : username,
		})

	def update_an_existing_user(self, user):
		db = MongoClient('localhost',3001).meteor
		usersCollection = db.users
		return usersCollection.update({'_id' : user['_id']}, {"$set" : user})

	def get_a_random_user(self):
		db = MongoClient('localhost',3001).meteor
		usersCollection = db.users
		usersCount = usersCollection.find({}).count()
		if usersCount == 0 :
			return None
		index = randint(0, usersCount-1)
		return usersCollection.find().limit(-1).skip(index).next()

	def insert_a_new_user(self, newUser):
		db = MongoClient('localhost',3001).meteor
		usersCollection = db.users
		return usersCollection.insert(newUser)
