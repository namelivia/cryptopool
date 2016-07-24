#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest2 as unittest
import mock
from poolsUpdater import PoolsUpdater
from lxml import html
from datetime import datetime 
from bson.objectid import ObjectId
import time
import io

#TODO: These tests could be better

class TestPoolsUpdater(unittest.TestCase):

	def setUp(self):
		self.poolsUpdater = PoolsUpdater()

	@mock.patch('scrapper_la_liga_oficial.poolsCollectionManager.PoolsCollectionManager.find_pools_by_match_id')
	@mock.patch('scrapper_la_liga_oficial.poolsUpdater.PoolsUpdater.update_pool')
	def test_updating_pools_for_a_match(self, mock_update_pool, mock_find_pools_by_match_id):
		matchId = 'foo';
		mock_find_pools_by_match_id.return_value = ['foo', 'bar', 'quix'];
		self.poolsUpdater.update_pools_for_a_match(matchId, 1, 0)
		mock_find_pools_by_match_id.assert_called_with(matchId)
		mock_update_pool.assert_called()

	@mock.patch('scrapper_la_liga_oficial.usersCollectionManager.UsersCollectionManager.find_user_by_id')
	@mock.patch('scrapper_la_liga_oficial.usersCollectionManager.UsersCollectionManager.update_an_existing_user')
	@mock.patch('scrapper_la_liga_oficial.poolsCollectionManager.PoolsCollectionManager.update_an_existing_pool')
	def test_updating_a_poll(self, mock_update_an_existing_pool, mock_update_an_existing_user, mock_find_user_by_id):
		user = { "_id" : "AWSYqjXtATexZwvT3", "tokens" : 7}
		mock_find_user_by_id.return_value = user;
		pool = {
			"amount" : 3,
			"status_id" : 0,
			"users" : [ 
				{ "_id" : "userId1","localScore" : 1,"visitantScore" : 0 }, 
				{ "_id" : "userId2","localScore" : 0,"visitantScore" : 1 }, 
				{ "_id" : "userId3","localScore" : 1,"visitantScore" : 0 }, 
				{ "_id" : "userId4","localScore" : 0,"visitantScore" : 0 }, 
				{ "_id" : "userId5","localScore" : 2,"visitantScore" : 0 }, 
			]
		}
		self.poolsUpdater.update_pool(pool, 1, 0)
		mock_find_user_by_id.assert_called()
		mock_update_an_existing_user.assert_called()
		mock_update_an_existing_pool.assert_called()

