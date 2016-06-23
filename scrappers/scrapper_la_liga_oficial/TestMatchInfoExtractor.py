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

	@mock.patch('scrapper_la_liga_oficial.matchInfoExtractor.MatchInfoExtractor.extract_hashtag')
	@mock.patch('scrapper_la_liga_oficial.matchInfoExtractor.MatchInfoExtractor.extract_referee')
	@mock.patch('scrapper_la_liga_oficial.matchInfoExtractor.MatchInfoExtractor.extract_team')
	@mock.patch('scrapper_la_liga_oficial.matchInfoExtractor.MatchInfoExtractor.extract_match_date')
	@mock.patch('scrapper_la_liga_oficial.matchInfoExtractor.MatchInfoExtractor.extract_score_and_status')
	def test_extracting_a_match_info(
		self,
		mock_extract_score_and_status,
		mock_extract_match_date,
		mock_extract_team,
		mock_extract_referee,
		mock_extract_hashtag
	):
		expectedMatchInfo = {
			'status': 1, 
			'player2': ObjectId('57109b1cc12fe22e66bfc09d'), 
			'player1': ObjectId('57109b1cc12fe22e66bfc09d'), 
			'score1': 1,
			'score2': 2,
			'hashtag': '#hashtag', 
			'date': datetime(2015, 10, 4, 2, 20, 19),
			'arbitro': 'RefereeName RefereeSurname'
		}
		mock_extract_score_and_status.return_value = (
				expectedMatchInfo['score1'],
				expectedMatchInfo['score2'],
				expectedMatchInfo['status']
		)
		mock_extract_match_date.return_value = expectedMatchInfo['date']
		mock_extract_team.return_value = expectedMatchInfo['player1'];
		#TODO: ¿Cómo que arbitro?
		mock_extract_referee.return_value = expectedMatchInfo['arbitro']
		mock_extract_hashtag.return_value = expectedMatchInfo['hashtag']
		htmlString = """
			<div class="partido even destacado">
            	<a href="http://www.laliga.es/directo/temporada-2015-2016/liga-bbva/38/valencia_real-sociedad" class="clearfix link_partido">
					<span class="fecha left"><span class='letra'>V</span><span class='dia'> 13-05-2016</span><span class='hora'> · 20:30</span></span>
					<span class="equipos clearfix left">
						<span class="equipo left local"><div class="escudo_comun sprite-escudos-xs valencia"> </div><span class="team">Valencia</span></span>
						<span class="hora-resultado left"><span class="horario-partido hora">0-1</span></span>
						<span class="equipo left visitante"><div class="escudo_comun sprite-escudos-xs real-sociedad"> </div><span class="team">R. Sociedad</span></span>
					 </span>
					 <span class="tv left"> Canal+ Liga/Abono Fútbol</span>
					 <span class="arbitro last">Velasco Carballo</span>
                 </a>
                 <div class="clear"></div>
             </div>
		""";
		match = html.fromstring(htmlString)
		counters = {
			'newMatchesCounter' : 0,
			'newTeamsCounter' : 0,
			'updatedMatchesCounter' : 0,
			'matchesWithoutHashtag' : 0,
			'matchesWithoutLink' : 0
		}
		result = self.matchInfoExtractor.fetch_match_info(match)
		#mock_extract_hashtag.assert_called_with(match, counters)
		mock_extract_referee.assert_called_with(match)
		#mock_extract_team.assert_called_with(match, True)
		#mock_extract_team.assert_called_with(match, False)
		mock_extract_match_date.assert_called_with(match)
		mock_extract_score_and_status.assert_called_with(match)
		self.assertEqual(expectedMatchInfo, result)

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
