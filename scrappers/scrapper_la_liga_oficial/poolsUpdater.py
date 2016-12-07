import logging
from poolsCollectionManager import PoolsCollectionManager
from usersCollectionManager import UsersCollectionManager
from notificationsCollectionManager import NotificationsCollectionManager
from datetime import datetime 

#TODO: This could have some more granularity, also for the tests

class PoolsUpdater:

	def __init__(self):
		self.logger = logging.getLogger("scrapperLaLigaOficial")
		self.poolsCollectionManager = PoolsCollectionManager()
		self.usersCollectionManager = UsersCollectionManager()
		self.notificationsCollectionManager = NotificationsCollectionManager()

	def update_pools_for_a_match(self, matchId, localScore, visitantScore):
		self.logger.debug('Updating the pools for the match')
		#find the pools for a match
		foundPools = self.poolsCollectionManager.find_pools_by_match_id(
				matchId
		)
		if foundPools is not None:
			for pool in foundPools:
				#decide the winner
				self.update_pool(pool, localScore, visitantScore, matchId)
		else:
			self.logger.debug('There are no pools for the match')
	
	def update_pool(self, pool, localScore, visitantScore, matchId):
		self.logger.debug('Updating pool')
		if pool['status_id'] == 1:
			self.logger.debug('The pool status is already 1, this is weird')
			return
		winners = []
		minDistance = None;
		#get the users that guessed the right score
		for user in pool['users']:
			#notify all the pool users that the pool has ended
			self.generate_pool_finished_notification(user['_id'],pool['_id'],matchId)
			distance = abs(user['localScore'] - localScore) + abs(user['visitantScore'] - visitantScore)
			if minDistance == None or distance < minDistance:
				minDistance = distance
			user['distance'] = distance
			if user['distance'] == 0:
				user['winner'] = True
				winners.append(user)
		if len(winners) == 0:
			if pool['options']['closest']:
				self.logger.debug('No one guessed the score, I should look for the closest bet')
				for user in pool['users']:
					if user['distance'] == minDistance :
						user['winner'] = True
						winners.append(user)
			else:
				self.logger.debug('No one guessed the score, everyone is a winner')
				winners = pool['users']
				for user in pool['users']:
					user['winner'] = True
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

	def generate_pool_finished_notification(self, userId, poolId, matchId):
		newNotification = {}
		newNotification['key'] = 'poolFinished'
		newNotification['user_id'] = userId
		newNotification['seen'] = False
		newNotification['createdAt'] = datetime.now()
		newNotification['data'] = {}
		newNotification['data']['matchId'] = str(matchId)
		newNotification['data']['poolId'] = str(poolId)
		self.notificationsCollectionManager.insert_a_new_notification(newNotification)
