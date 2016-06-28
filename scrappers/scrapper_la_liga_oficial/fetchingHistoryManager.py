from pymongo import MongoClient

class FetchingHistoryManager:

	def find_a_record(self, url):
		db = MongoClient('localhost',3001).meteor
		recordsCollection = db.scrapperLaLigaOficialRecords
		return recordsCollection.find_one({
			'url' : url
		})

	def insert_a_new_record(self, url):
		db = MongoClient('localhost',3001).meteor
		recordsCollection = db.scrapperLaLigaOficialRecords
		return recordsCollection.insert({
			'url' : url
		})
