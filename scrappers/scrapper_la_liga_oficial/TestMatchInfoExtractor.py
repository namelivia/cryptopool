#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest2 as unittest
import mock
import mongomock
from matchInfoExtractor import MatchInfoExtractor
from lxml import html
from datetime import datetime 
from bson.objectid import ObjectId
import time
import io

class TestMatchInfoExtractor(unittest.TestCase):

	def setUp(self):
		self.matchInfoExtractor = MatchInfoExtractor()

	def test_extracting_the_referee_from_a_match(self):
		htmlString = """
		fooBarfooBar
			<span class="arbitro last">Referee1</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		self.assertEqual('Referee1',self.matchInfoExtractor.extract_referee(tree))

	def test_extracting_the_match_date_and_hour(self):
		htmlString = """
		fooBarfooBar
			<span class="fecha left">
				<span class="dia">15-12-2016</span>
				<span class="hora">aa12:00 </span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		matchDate = self.matchInfoExtractor.extract_match_date(tree)
		expectedDate = datetime(2016, 12, 15, 12, 00, 00)
		self.assertEqual(expectedDate,matchDate)

	def test_extracting_the_match_date_without_hour(self):
		htmlString = """
		fooBarfooBar
			<span class="fecha left">
				<span class="dia">15-12-2016</span>
				<span class="hora"></span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		matchDate = self.matchInfoExtractor.extract_match_date(tree)
		expectedDate = datetime(2016, 12, 15, 00, 00, 00)
		self.assertEqual(expectedDate,matchDate)

	@mock.patch('scrapper_la_liga_oficial.teamsCollectionManager.TeamsCollectionManager.find_a_team_by_name')
	def test_extracting_the_local_team_from_a_match_when_the_team_is_present(
			self,
			mock_find_a_team_by_name
		):
		mock_find_a_team_by_name.return_value = {
				'_id': 'foo',
				'name' : 'FooTeam'
		}
		htmlString = """
		fooBarfooBar
			<span class="equipo left local">
				<span class="team">FooTeam</span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		newTeam = self.matchInfoExtractor.extract_team(tree,True)
		self.assertEqual('foo',newTeam)

	@mock.patch('scrapper_la_liga_oficial.teamsCollectionManager.TeamsCollectionManager.insert_a_new_team')
	@mock.patch('scrapper_la_liga_oficial.teamsCollectionManager.TeamsCollectionManager.find_a_team_by_name')
	def test_extracting_the_local_team_from_a_match_when_the_team_is_not_present(
			self,
			mock_find_a_team_by_name,
			mock_insert_a_new_team
		):
		mock_find_a_team_by_name.return_value = None
		mock_insert_a_new_team.return_value = 'newTeamId'
		htmlString = """
		fooBarfooBar
			<span class="equipo left local">
				<span class="team">FooTeam</span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		newTeamId = self.matchInfoExtractor.extract_team(tree,True)
		mock_insert_a_new_team.assert_called_with({
			'name' : 'FooTeam',
			'tag' : 'footeam'
		})
		self.assertEqual('newTeamId', newTeamId)

#	def test_tag_formation_for_spaces(self):
#		teamsCollection = mongomock.MongoClient().db.collection
#		htmlString = """
#		fooBarfooBar
#			<span class="equipo left local">
#				<span class="team">Foo Team</span>
#			</span>
#		fooBarfooBar
#		""";
#		tree = html.fromstring(htmlString)
##		newTeam = self.matchInfoExtractor.extract_team(tree,True)
#		insertedTeam = teamsCollection.find_one({'_id' : newTeam}) 
#		self.assertEqual('Foo Team',insertedTeam['name'])
#		self.assertEqual('foo_team',insertedTeam['tag'])
#
#	def test_tag_formation_for_points(self):
#		teamsCollection = mongomock.MongoClient().db.collection
#		htmlString = """
#		fooBarfooBar
#			<span class="equipo left local">
#				<span class="team">Fc. Foo Team</span>
#			</span>
#		fooBarfooBar
#		""";
#		tree = html.fromstring(htmlString)
#		newTeam = self.matchInfoExtractor.extract_team(tree,True)
#		insertedTeam = teamsCollection.find_one({'_id' : newTeam}) 
#		self.assertEqual('Fc. Foo Team',insertedTeam['name'])
#		self.assertEqual('fc_foo_team',insertedTeam['tag'])
#
#	def test_tag_formation_for_the_real_keyword(self):
#		teamsCollection = mongomock.MongoClient().db.collection
##		htmlString = """
#		fooBarfooBar
#			<span class="equipo left local">
#				<span class="team">R. Foo Team</span>
#			</span>
#		fooBarfooBar
#		""";
#		tree = html.fromstring(htmlString)
#		newTeam = self.matchInfoExtractor.extract_team(tree,True)
#		insertedTeam = teamsCollection.find_one({'_id' : newTeam}) 
#		self.assertEqual('R. Foo Team',insertedTeam['name'])
#		self.assertEqual('real_foo_team',insertedTeam['tag'])
#
	@mock.patch('scrapper_la_liga_oficial.matchInfoExtractor.requests.post')
	def test_extracting_the_match_hashtag(self, mock_requests_get):
		link = 'http://match_details_url'
		mock_requests_get.return_value.text = """"
		fooBar
		<div id="hashtag">#hashtag</div>
		fooBar
		"""
		hashtag = self.matchInfoExtractor.extract_hashtag(link)
		self.assertEqual('#hashtag', hashtag)

	def test_extracting_the_score_and_the_status(self):
		htmlString = """
		fooBarfooBar
			<span class="hora-resultado left">
				<span class="horario-partido hora">0-1</span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		result = self.matchInfoExtractor.extract_score_and_status(tree);
		self.assertEqual(('0', '1', 1),result);

if __name__ == '__main__':
	unittest.main()
