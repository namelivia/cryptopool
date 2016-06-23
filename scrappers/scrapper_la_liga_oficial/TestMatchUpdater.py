#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest2 as unittest
import mock
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
	@mock.patch('scrapper_la_liga_oficial.matchesCollectionManager.MatchesCollectionManager.find_a_match')
	def test_creation_creating_or_updating_a_match(self, mock_find_a_match, mock_update_match_if_needed, mock_insert_a_new_match):
		#creating
		mock_find_a_match.return_value = None
		match = {
			'player1' : '57109b1dc12fe22e66bfc0a7',
			'player2' : '57109b1ec12fe22e66bfc0b2',
			'date' : 'quix'
		}
		result = self.matchUpdater.create_or_update_the_match(match)
		mock_find_a_match.assert_called_with(match['player1'], match['player2'], match['date'])
		mock_insert_a_new_match.assert_called_with(match)

		#updating
		mock_find_a_match.return_value = match
		result = self.matchUpdater.create_or_update_the_match(match)
		mock_find_a_match.assert_called_with(match['player1'], match['player2'], match['date'])
		mock_update_match_if_needed.assert_called_with(match,match)

	@mock.patch('scrapper_la_liga_oficial.matchesCollectionManager.MatchesCollectionManager.insert_a_new_match')
	@mock.patch('scrapper_la_liga_oficial.executionCounters.ExecutionCounters.increase_new_matches_counter')
	def test_inserting_a_new_match(self, mock_increase_new_matches_counter, mock_insert_a_new_match):
		match = {
			'player1' : '57109b1dc12fe22e66bfc0a7',
			'player2' : '57109b1ec12fe22e66bfc0b2',
			'date' : 'quix'
		}
		result = self.matchUpdater.insert_a_new_match(match)
		mock_insert_a_new_match.assert_called_with(match)
		mock_increase_new_matches_counter.assert_called_with()

	@mock.patch('scrapper_la_liga_oficial.matchesCollectionManager.MatchesCollectionManager.update_an_existing_match')
	@mock.patch('scrapper_la_liga_oficial.executionCounters.ExecutionCounters.increase_updated_matches_counter')
	def test_inserting_a_new_match(self, mock_increase_updated_matches_counter, mock_update_an_existing_match):
		match = {
			'player1' : '57109b1dc12fe22e66bfc0a7',
			'player2' : '57109b1ec12fe22e66bfc0b2',
			'date' : 'quix',
			'score1' : '',
			'score2' : '',
			'status' : '0'
		}
		updatedMatch = {
			'player1' : '57109b1dc12fe22e66bfc0a7',
			'player2' : '57109b1ec12fe22e66bfc0b2',
			'date' : 'quix',
			'score1' : '2',
			'score2' : '0',
			'status' : '1'
		}
		result = self.matchUpdater.update_match_if_needed(match,updatedMatch)
		mock_update_an_existing_match.assert_called_with(updatedMatch)
		mock_increase_updated_matches_counter.assert_called_with()

if __name__ == '__main__':
	unittest.main()
