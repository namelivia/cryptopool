import logging
from executionCounters import ExecutionCounters
from matchesCollectionManager import MatchesCollectionManager

class MatchUpdater:

	def __init__(self):
		self.matchesCollectionManager = MatchesCollectionManager()
		self.executionCounters = ExecutionCounters()

#Creates or updates a match on the database
	def create_or_update_the_match(self, match):
		logger = logging.getLogger("scrapperLaLigaOficial")
		foundMatch = self.matchesCollectionManager.find_a_match(
				match['player1'],
				match['player2'],
				match['date']
		)
		if foundMatch is None:
			logger.debug('Inserting a new match')
			self.insert_a_new_match(match)
		else : 
			logger.debug('Updating an existing match if needed')
			self.update_match_if_needed(foundMatch,match)

#Insert a new match in the database
	def insert_a_new_match(self,match):
		self.matchesCollectionManager.insert_a_new_match(match)
		self.executionCounters.increase_new_matches_counter()

#Update the match if needed
	def update_match_if_needed(self,foundMatch,match):
		if (foundMatch['score1'] == match['score1'] and foundMatch['score2'] == match['score2'] and foundMatch['status'] == match['status']) :
			return 
		foundMatch['score1'] = match['score1']
		foundMatch['score2'] = match['score2']
		foundMatch['status'] = match['status']
		self.matchesCollectionManager.update_an_existing_match(foundMatch)
		self.executionCounters.increase_updated_matches_counter()
