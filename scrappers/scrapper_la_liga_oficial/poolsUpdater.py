import logging
class PoolsUpdater:
	def __init__(self):
		self.logger = logging.getLogger("scrapperLaLigaOficial")
	def update_pools_for_a_match(self, matchId):
		self.logger.debug('I am updating some pools')
