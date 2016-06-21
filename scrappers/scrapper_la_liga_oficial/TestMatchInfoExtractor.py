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

	def test_extracting_the_local_team_from_a_match_when_the_team_is_present(self):
		teams = [dict(name="FooTeam")];
		teamsCollection = mongomock.MongoClient().db.collection
		for team in teams:
			team['_id'] = teamsCollection.insert(team)
		htmlString = """
		fooBarfooBar
			<span class="equipo left local">
				<span class="team">FooTeam</span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		newTeam = self.matchInfoExtractor.extract_team(tree,True,teamsCollection,5)
		self.assertEqual(5,newTeam[0])
		self.assertEqual(teams[0]['_id'],newTeam[1])

	def test_extracting_the_local_team_from_a_match_when_the_team_is_not_present(self):
		teamsCollection = mongomock.MongoClient().db.collection
		htmlString = """
		fooBarfooBar
			<span class="equipo left local">
				<span class="team">FooTeam</span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		newTeam = self.matchInfoExtractor.extract_team(tree,True,teamsCollection,5)
		self.assertEqual(6,newTeam[0])
		insertedTeam = teamsCollection.find_one({'_id' : newTeam[1]}) 
		self.assertEqual('FooTeam',insertedTeam['name'])
		self.assertEqual('footeam',insertedTeam['tag'])

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

	def test_tag_formation_for_spaces(self):
		teamsCollection = mongomock.MongoClient().db.collection
		htmlString = """
		fooBarfooBar
			<span class="equipo left local">
				<span class="team">Foo Team</span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		newTeam = self.matchInfoExtractor.extract_team(tree,True,teamsCollection,5)
		self.assertEqual(6,newTeam[0])
		insertedTeam = teamsCollection.find_one({'_id' : newTeam[1]}) 
		self.assertEqual('Foo Team',insertedTeam['name'])
		self.assertEqual('foo_team',insertedTeam['tag'])

	def test_tag_formation_for_points(self):
		teamsCollection = mongomock.MongoClient().db.collection
		htmlString = """
		fooBarfooBar
			<span class="equipo left local">
				<span class="team">Fc. Foo Team</span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		newTeam = self.matchInfoExtractor.extract_team(tree,True,teamsCollection,5)
		self.assertEqual(6,newTeam[0])
		insertedTeam = teamsCollection.find_one({'_id' : newTeam[1]}) 
		self.assertEqual('Fc. Foo Team',insertedTeam['name'])
		self.assertEqual('fc_foo_team',insertedTeam['tag'])

	def test_tag_formation_for_the_real_keyword(self):
		teamsCollection = mongomock.MongoClient().db.collection
		htmlString = """
		fooBarfooBar
			<span class="equipo left local">
				<span class="team">R. Foo Team</span>
			</span>
		fooBarfooBar
		""";
		tree = html.fromstring(htmlString)
		newTeam = self.matchInfoExtractor.extract_team(tree,True,teamsCollection,5)
		self.assertEqual(6,newTeam[0])
		insertedTeam = teamsCollection.find_one({'_id' : newTeam[1]}) 
		self.assertEqual('R. Foo Team',insertedTeam['name'])
		self.assertEqual('real_foo_team',insertedTeam['tag'])

	@mock.patch('scrapper_la_liga_oficial.matchInfoExtractor.requests.post')
	def test_extracting_the_match_hashtag(self, mock_requests_get):
		link = 'http://match_details_url'
		matchesWithoutHashtagCount = 0
		mock_requests_get.return_value.text = """"
		fooBar
		<div id="hashtag">#hashtag</div>
		fooBar
		"""
		hashtag = self.matchInfoExtractor.extract_hashtag(link,matchesWithoutHashtagCount)
		self.assertEqual((matchesWithoutHashtagCount,'#hashtag'), hashtag)

if __name__ == '__main__':
	unittest.main()
