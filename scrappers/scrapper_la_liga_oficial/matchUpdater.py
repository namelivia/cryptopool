import logging
from bson.objectid import ObjectId
from executionCounters import ExecutionCounters

class MatchUpdater:

#Creates or updates a match on the database
	def create_or_update_the_match(self, matchesCollection, match):
		logger = logging.getLogger("scrapperLaLigaOficial")
		foundMatch = matchesCollection.find_one({
			"player1" : ObjectId(match['player1']),
			"player2" : ObjectId(match['player2']),
			"date" : match['date']
		})
		if foundMatch is None:
			logger.debug('Inserting a new match')
			self.insert_a_new_match(matchesCollection,match)
		else : 
			logger.debug('Updating an existing match if needed')
			self.update_match_if_needed(matchesCollection,foundMatch,match)

#Insert a new match in the database
	def insert_a_new_match(self,matchesCollection,match,newMatchesCounter):
		matchesCollection.insert(match)
		executionCounters = ExecutionCounters()
		executionCounters.increase_new_matches_counter()

#Update the match if needed
	def update_match_if_needed(self,matchesCollection,foundMatch,match,updatedMatchesCounter):
		if (foundMatch['score1'] == match['score1'] and foundMatch['score2'] == match['score2'] and foundMatch['status'] == match['status']) :
			return updatedMatchesCounter
		foundMatch['score1'] = match['score1']
		foundMatch['score2'] = match['score2']
		foundMatch['status'] = match['status']
		matchesCollection.update({'_id' : foundMatch['_id']}, {"$set" : foundMatch})
		executionCounters = ExecutionCounters()
		executionCounters.increase_updated_matches_counter()
