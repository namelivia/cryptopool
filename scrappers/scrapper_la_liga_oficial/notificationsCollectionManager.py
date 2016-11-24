from pymongo import MongoClient
from bson.objectid import ObjectId
from random import randint

class NotificationsCollectionManager:

	def insert_a_new_notification(self, newNotification):
		db = MongoClient('localhost',3001).meteor
		notificationsCollection = db.notifications
		return notificationsCollection.insert(newNotification)
