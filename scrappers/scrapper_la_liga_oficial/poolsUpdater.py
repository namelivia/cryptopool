import logging
from poolsCollectionManager import PoolsCollectionManager
from usersCollectionManager import UsersCollectionManager

#TODO: This could have some more granularity, also for the tests

class PoolsUpdater:

	def __init__(self):
		self.logger = logging.getLogger("scrapperLaLigaOficial")
		self.poolsCollectionManager = PoolsCollectionManager()
		self.usersCollectionManager = UsersCollectionManager()

	def update_pools_for_a_match(self, matchId, localScore, visitantScore):
		self.logger.debug('Updating the pools for the match')
		#find the pools for a match
		foundPools = self.poolsCollectionManager.find_pools_by_match_id(
				matchId
		)
		if foundPools is not None:
			for pool in foundPools:
				#decide the winner
				self.update_pool(pool, localScore, visitantScore)
		else:
			self.logger.debug('There are no pools for the match')
	
	def update_pool(self, pool, localScore, visitantScore):
		self.logger.debug('Updating pool')
		if pool['status_id'] == 1:
			self.logger.debug('The pool status is already 1, this is weird')
			return
		winners = []
		#get the users that guessed the right score
		for user in pool['users']:
			if user['localScore'] == localScore and user['visitantScore'] == visitantScore:
				winners.append(user)
		if len(winners) == 0:
			self.logger.debug('No one guessed the score, everyone is a winner')
			winners = pool['users']
		if len(pool['users']) > 0:
			#share the price with those users
			prize = float(pool['amount'])*len(pool['users'])/len(winners)
			self.logger.debug('The total amount is :'+str(pool['amount']*len(pool['users'])))
			self.logger.debug('The number of winners is:'+str(len(winners)))
			self.logger.debug('The prize is :'+str(prize))
			for winner in winners:
				foundUser = self.usersCollectionManager.find_user_by_id(winner['_id'])
				self.logger.debug('The user '+str(winner['_id'])+' is a winner.')
				self.logger.debug('Has '+str(foundUser['tokens'])+' tokens.')
				foundUser['tokens'] += prize
				self.logger.debug('Now has '+str(foundUser['tokens'])+' tokens.')
				self.usersCollectionManager.update_an_existing_user(foundUser)
		#update the pool
		pool['status_id'] = 1
		self.poolsCollectionManager.update_an_existing_pool(pool)
