import logging
import pprint
from executionCounters import ExecutionCounters
from matchesCollectionManager import MatchesCollectionManager

class MatchUpdater:

	def __init__(self):
		self.matchesCollectionManager = MatchesCollectionManager()
		self.executionCounters = ExecutionCounters()
		self.logger = logging.getLogger("scrapperLaLigaOficial")

	def create_or_update_the_match(self, match):
		foundMatch = self.matchesCollectionManager.find_a_match(
				match['player1'],
				match['player2'],
				match['date']
		)
		if foundMatch is None:
			self.insert_a_new_match(match)
		else : 
			self.update_match_if_needed(foundMatch,match)

	def insert_a_new_match(self,match):
		self.logger.debug('I have a new match, will insert it')
		self.logger.debug(pprint.pformat(match))
		self.matchesCollectionManager.insert_a_new_match(match)
		self.executionCounters.increase_new_matches_counter()

	def update_match_if_needed(self,foundMatch,match):
		if (foundMatch['score1'] == match['score1'] and foundMatch['score2'] == match['score2'] and foundMatch['status'] == match['status']) :
			self.logger.debug('The match is already in the database, skipping it')
			return 
		self.logger.debug('The match has changed, will update it')
		self.logger.debug('Old match version')
		self.logger.debug(pprint.pformat(foundMatch))
		self.logger.debug('New match version')
		self.logger.debug(pprint.pformat(match))
		foundMatch['score1'] = match['score1']
		foundMatch['score2'] = match['score2']
		foundMatch['status'] = match['status']
		self.matchesCollectionManager.update_an_existing_match(foundMatch)
		self.executionCounters.increase_updated_matches_counter()
