from pymongo import MongoClient

class FetchingHistoryManager:
	def __init__(self): 
		db = MongoClient('localhost',3001).meteor
		self.recordsCollection = db.scrapperLaLigaOficialRecords

	def find_a_record(self, url):
		return self.recordsCollection.find_one({
			'url' : url
		})

	def insert_a_new_record(self, url):
		return self.recordsCollection.insert({
			'url' : url
		})
