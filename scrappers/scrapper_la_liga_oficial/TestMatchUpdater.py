#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest2 as unittest
import mock
import mongomock
from matchUpdater import MatchUpdater
from lxml import html
from datetime import datetime 
from bson.objectid import ObjectId
import time
import io

class TestMatchUpdater(unittest.TestCase):

	def setUp(self):
		self.matchUpdater = MatchUpdater()

	@mock.patch('scrapper_la_liga_oficial.matchUpdater.MatchUpdater.insert_a_new_match')
	@mock.patch('scrapper_la_liga_oficial.matchUpdater.MatchUpdater.update_match_if_needed')
	def test_creation_creating_or_updating_a_match(self, mock_update_match_if_needed, mock_insert_a_new_match):
		#creating
		mock_insert_a_new_match.return_value = 1
		mock_update_match_if_needed.return_value = 1
		matchesCollection = mongomock.MongoClient().db.collection
		match = {
			'player1' : '57109b1dc12fe22e66bfc0a7',
			'player2' : '57109b1ec12fe22e66bfc0b2',
			'date' : 'quix'
		}
		result = self.matchUpdater.create_or_update_the_match(matchesCollection, match)
		#TODO: Expectancies for this

		#updating
		matchesCollection.insert({
			"player1" : ObjectId(match['player1']),
			"player2" : ObjectId(match['player2']),
			"date" : match['date']
		})
		result = self.matchUpdater.create_or_update_the_match(matchesCollection, match)
		#TODO: Expectancies for this
if __name__ == '__main__':
	unittest.main()
