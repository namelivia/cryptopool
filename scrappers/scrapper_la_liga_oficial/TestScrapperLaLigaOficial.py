#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest2 as unittest
import mock
import mongomock
from scrapperLaLigaOficial import ScrapperLaLigaOficial
from lxml import html
from datetime import datetime 
from bson.objectid import ObjectId
import time
import io

class TestScrapperLaLigaOficial(unittest.TestCase):

	def setUp(self):
		self.scrapper = ScrapperLaLigaOficial()

	def test_finding_the_data_on_the_page(self):
		page = """
		<html>
			<script>script1</script>
			<script>script2script2script2</script>
			<script>
				script3
				script3
				script3
				0123456789012345script3longestline78
			</script>
			<script>script4</script>
			<script>script5</script>
			<script>script6</script>
			<script>script7</script>
			<script>script8</script>
		</html>
		"""
		data = self.scrapper.data_find(page)
		self.assertEqual('script3longestline',data)

	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.MatchInfoExtractor.extract_hashtag')
	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.MatchInfoExtractor.extract_referee')
	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.MatchInfoExtractor.extract_team')
	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.MatchInfoExtractor.extract_match_date')
	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.MatchInfoExtractor.extract_score_and_status')
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
		result = self.scrapper.fetch_match_info(match)
		#mock_extract_hashtag.assert_called_with(match, counters)
		mock_extract_referee.assert_called_with(match)
		#mock_extract_team.assert_called_with(match, True)
		#mock_extract_team.assert_called_with(match, False)
		mock_extract_match_date.assert_called_with(match)
		mock_extract_score_and_status.assert_called_with(match)
		self.assertEqual(expectedMatchInfo, result)

	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.time.time')
	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.requests.get')
	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.requests.post')
	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.ScrapperLaLigaOficial.data_find')
	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.ScrapperLaLigaOficial.fetch_match_info')
	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.MatchUpdater.create_or_update_the_match')
	def test_scrapping(
			self,
			mock_create_or_update_the_match,
			mock_fetch_match_info,
			mock_data_find,
			mock_requests_post,
			mock_requests_get,
			mock_time
		):
		calendarUrl = 'http://www.laliga.es/calendario-horario/';
		eventId = u'#1_1_1_10_8_2016';
		eventUrl = 'http://www.laliga.es/includes/ajax.php?action=ver_evento_calendario';
		match = html.fromstring("<div></div>");
		matchInfo = {
				'foo' : 'bar'
		}
		counters = {
			'newMatchesCounter' : 0,
			'newTeamsCounter' : 0,
			'updatedMatchesCounter' : 0,
			'matchesWithoutHashtag' : 0,
			'matchesWithoutLink' : 0
		}

		mock_fetch_match_info.return_value = matchInfo
		mock_data_find.return_value = '[{"url" : "'+eventId+'"}]'
		mock_requests_get.return_value.text = self.get_html_example(calendarUrl)
		mock_requests_post.return_value.text = self.get_html_example(eventUrl)
		mock_time.return_value = time.mktime(datetime(2016, 8, 15, 12, 00, 00).timetuple())
		self.scrapper = ScrapperLaLigaOficial()
		test = self.scrapper.start_scrapping(5)
		mock_time.assert_called_with()
		mock_requests_get.assert_called_with(calendarUrl)
		mock_requests_post.assert_called_with(eventUrl, data={'filtro': eventId})
		mock_requests_post.assert_called_with(eventUrl, data={'filtro': eventId})
		#TODO
		#mock_fetch_match_info.assert_called_with(match)

	#Aux functions
	def get_html_example(self, url):
		examples = {
			'http://www.laliga.es/calendario-horario/' : 'calendario-horario.html',
			'http://www.laliga.es/includes/ajax.php?action=ver_evento_calendario' : 'ver-evento-calendario.html',
		}
		with io.open('request_examples/'+examples[url], 'r', encoding='utf-8') as myfile:
			data = myfile.read().replace('\n', '')
		return data

if __name__ == '__main__':
	unittest.main()
