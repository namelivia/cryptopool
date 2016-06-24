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

	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.time.time')
	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.requests.get')
	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.ScrapperLaLigaOficial.data_find')
	@mock.patch('scrapper_la_liga_oficial.eventsFetcher.EventsFetcher.check_if_an_event_has_already_been_fetched')
	@mock.patch('scrapper_la_liga_oficial.eventsFetcher.EventsFetcher.fetch_an_event')
	def test_scrapping(
			self,
			mock_fetch_an_event,
			mock_check_if_an_event_has_already_been_fetched,
			mock_data_find,
			mock_requests_get,
			mock_time
		):
		calendarUrl = 'http://www.laliga.es/calendario-horario/';
		event = {
				'url': '#1_1_1_10_8_2016'
		}
		match = html.fromstring("<div></div>");
		counters = {
			'newMatchesCounter' : 0,
			'newTeamsCounter' : 0,
			'updatedMatchesCounter' : 0,
			'matchesWithoutHashtag' : 0,
			'matchesWithoutLink' : 0
		}
		dateRange = 5

		mock_data_find.return_value = '[{"url" : "'+event['url']+'"}]'
		mock_time.return_value = time.mktime(datetime(2016, 8, 15, 12, 00, 00).timetuple())
		mock_check_if_an_event_has_already_been_fetched.return_value = False
		self.scrapper = ScrapperLaLigaOficial()
		test = self.scrapper.start_scrapping(dateRange)
		mock_time.assert_called_with()
		mock_requests_get.assert_called_with(calendarUrl)
		mock_check_if_an_event_has_already_been_fetched.assert_called_with(event, dateRange)
		mock_fetch_an_event.assert_called_with(event)

if __name__ == '__main__':
	unittest.main()
