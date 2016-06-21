import logging
from bson.objectid import ObjectId

class MatchUpdater:

#Creates or updates a match on the database
	def create_or_update_the_match(self, matchesCollection, match, newMatchesCounter, updatedMatchesCounter):
		logger = logging.getLogger("scrapperLaLigaOficial")
		foundMatch = matchesCollection.find_one({
			"player1" : ObjectId(match['player1']),
			"player2" : ObjectId(match['player2']),
			"date" : match['date']
		})
		if foundMatch is None:
			logger.debug('Inserting a new match')
			newMatchesCounter = self.insert_a_new_match(matchesCollection,match,newMatchesCounter)
		else : 
			logger.debug('Updating an existing match if needed')
			updatedMatchesCounter = self.update_match_if_needed(matchesCollection,foundMatch,match,updatedMatchesCounter)
		return (newMatchesCounter, updatedMatchesCounter)

#Insert a new match in the database
	def insert_a_new_match(self,matchesCollection,match,newMatchesCounter):
		matchesCollection.insert(match)
		return newMatchesCounter + 1

#Update the match if needed
	def update_match_if_needed(self,matchesCollection,foundMatch,match,updatedMatchesCounter):
		if (foundMatch['score1'] == match['score1'] and foundMatch['score2'] == match['score2'] and foundMatch['status'] == match['status']) :
			return updatedMatchesCounter
		foundMatch['score1'] = match['score1']
		foundMatch['score2'] = match['score2']
		foundMatch['status'] = match['status']
		matchesCollection.update({'_id' : foundMatch['_id']}, {"$set" : foundMatch})
		#TODO
		#self.update_match_pools(foundMatch['_id'], match['score1'], match['score2']);
		return updatedMatchesCounter + 1
