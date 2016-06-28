from pymongo import MongoClient
from bson.objectid import ObjectId

class ReportsGenerator:

	reportHtml = u'<html>'

	def generate_insert_match_record(self, match):
		self.reportHtml += u'Inserting a new match'
		self.reportHtml += self.printItems(match, 0)
		self.reportHtml += u'<hr></hr>'

	def generate_insert_match_record(self, match):
		self.reportHtml += 'Updating an existing match'
		self.reportHtml += self.printItems(match, 0)
		self.reportHtml += u'<hr></hr>'

	def printItems(self, dictObj, indent):
		result = u''
		result += u'  '*indent
		result += u'<ul>\n'
		for k,v in dictObj.iteritems():
			if isinstance(v, dict):
				result += u' '*ident
				result += u'<li>{0}</li>'.format(k)
				printItems(v, indent+1)
			else:
				result += u' '*indent
				result += u'<li>{0}:{1}</li>'.format(k,v)
		result += u'  '*indent
		result += u'</ul>\n'
		return result

	def printHtmlContent(self):
		print(self.reportHtml)
