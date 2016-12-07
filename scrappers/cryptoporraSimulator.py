#!/usr/bin/python
# -*- coding: utf-8 -*-
from scrapper_la_liga_oficial.matchUpdater import MatchUpdater
from scrapper_la_liga_oficial.usersCollectionManager import UsersCollectionManager
from scrapper_la_liga_oficial.poolsCollectionManager import PoolsCollectionManager
from scrapper_la_liga_oficial.teamsCollectionManager import TeamsCollectionManager
from scrapper_la_liga_oficial.matchesCollectionManager import MatchesCollectionManager
import random
from random import randint
import string
from faker import Faker
import datetime
import pprint
import logging
import os
import time

class CryptoporraSimulator:
	def __init__(self):
		self.faker = Faker()
		self.usersCollectionManager = UsersCollectionManager()
		self.poolsCollectionManager = PoolsCollectionManager()
		self.matchesCollectionManager = MatchesCollectionManager()
		self.teamsCollectionManager = TeamsCollectionManager()
		self.matchUpdater = MatchUpdater()
		self.logger = self.init_logger()

	def init_logger(self):
		stderrLogger=logging.StreamHandler()
		logging.getLogger().addHandler(stderrLogger)
		stderrLogger.setLevel(logging.INFO)
		logging.getLogger("requests").setLevel(logging.WARNING)
		logger = logging.getLogger("CryptoporraSimulator")
		execPath = os.path.dirname(os.path.realpath(__file__))
		handler = logging.FileHandler(execPath+"/logs/CryptoporraSimulator-{0}.log".format(int(time.time())))
		logger.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		logger.addHandler(handler)
		return logger

	def simulation_step(self):
			self.logger.debug('Simulation step')
			operation = randint(0, 10)
			if operation == 0:
				self.create_a_random_match()
			if operation == 1:
				self.random_update_a_match()
			if operation > 1 and operation < 8:
				self.make_a_random_bet()
			if operation == 9:
				self.make_a_random_pool()
			if operation == 10:
				self.make_a_random_user()

	def make_a_random_user(self):
		self.logger.debug('Creating a random user')
		email = self.faker.email()
		username = self.faker.word()
		foundUser = self.usersCollectionManager.find_user_by_username(username)
		if foundUser is None :
			newUser = {
					"services" : { 
						"password" : { "bcrypt" : "$2a$10$VxfCnQmcDKYcIGy0C3eecOehWuvQ3lWLWPga7peJKJY1hXf1qqhzu" },
						"email" : { 
							"verificationTokens" : []
						},
						"resume" : { 
							"loginTokens" : [ ] 
						} 
					},
					"_id" : ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(17)),
					"username" : username,
					"emails" : [ { "verified" : True, "address" : email} ],
					"tokens" : 10, "poolHistory" : [] }
			self.usersCollectionManager.insert_a_new_user(newUser)
			self.logger.debug('New user created')
			self.logger.debug(pprint.pformat(newUser))
		else:
			self.logger.debug('The username I wanted to use is already taken')

	def make_a_random_pool(self):
		self.logger.debug('Creating a random pool')
		#pick a random user
		user = self.usersCollectionManager.get_a_random_user()
		if user is not None :
			match = self.matchesCollectionManager.get_a_random_unplayed_match()
			if match is not None :
				newPool = {
					"amount" :randint(1, 9),
					"match_id" : match['_id'],
					"status_id" : 0,
					"user_id" : user['_id'],
					"allowed_users" : [{"id" : user['_id'], "confirmed" : True}],
					"users" : [],
					"options" : [{"is_private" : False, "multiuser" : True, "multiscore" : False, "closest" : False}],
					"matchDate" : match['date']
				}
				self.poolsCollectionManager.insert_a_new_pool(newPool)
				self.logger.debug('Random pool created')
				self.logger.debug(pprint.pformat(newPool))
			else:
				self.logger.debug('There are no matches for creating the pool')
		else:
			self.logger.debug('There are no users for creating the pool')

	def create_a_random_match(self):
		self.logger.debug('Creating a random match')
		player1Id = self.teamsCollectionManager.get_a_random_team()['_id'];
		player2Id = self.teamsCollectionManager.get_a_random_team()['_id'];
		if player1Id is not None and player2Id is not None :
			match = {
				'player1' : player1Id,
				'player2' : player2Id,
				'date' : datetime.datetime.now() - datetime.timedelta(days=1),
				'score1' : '',
				'score2' : '',
				'status' : 0,
				'referee' : self.faker.name(),
				'hashtag' : '#Madrid'
			}
			self.matchUpdater.create_or_update_the_match(match)
			self.logger.debug('New match created')
			self.logger.debug(pprint.pformat(match))
		else:
			self.logger.debug('There are no teams for creating the match')

	def random_update_a_match(self):
		self.logger.debug('Random updating a match')
		match = self.matchesCollectionManager.get_a_random_unplayed_match()
		if match is not None :
			match['score1'] = randint(0,3)
			match['score2'] = randint(0,3)
			match['status'] = 1
			self.matchUpdater.create_or_update_the_match(match)
			self.logger.debug('Random match updated')
			self.logger.debug(pprint.pformat(match))
		else:
			self.logger.debug('There are no matches to update')

	def make_a_random_bet(self):
		self.logger.debug('Making a random bet')
		user = self.usersCollectionManager.get_a_random_user()
		if user is not None :
			pool = self.poolsCollectionManager.get_a_random_open_pool_for_tokens(user['tokens'])
			#TODO: This way a user can participate twice on a bet, this should not be allowed
			if pool is not None :
				user['tokens'] -= pool['amount']
				user['poolHistory'].append(pool['_id'])
				newEntry = {
						'_id' : user['_id'],
						'localScore' : randint(0,3),
						'visitantScore' : randint(0,3)
				}
				pool['users'].append(newEntry)
				self.logger.debug('New bet created')
				self.logger.debug(pprint.pformat(newEntry))
				self.usersCollectionManager.update_an_existing_user(user)
				self.poolsCollectionManager.update_an_existing_pool(pool)
			else:
				self.logger.debug('There are no pools for making the bet')
		else:
			self.logger.debug('There are no users for making the bet')
