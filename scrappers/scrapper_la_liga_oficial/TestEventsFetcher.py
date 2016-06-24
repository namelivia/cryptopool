#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest2 as unittest
import mock
from eventsFetcher import EventsFetcher
import io

class TestEventsFetcher(unittest.TestCase):

	def setUp(self):
		self.eventsFetcher = EventsFetcher()

	@mock.patch('scrapper_la_liga_oficial.fetchingHistoryManager.FetchingHistoryManager.find_a_record')
	def test_checking_that_an_event_has_already_been_fetched(
			self,
			mock_find_a_record
	):
		event = {
				'url': '#1_1_1_10_8_2016'
		}
		dateRange = 5;
		result = self.eventsFetcher.check_if_an_event_has_already_been_fetched(event,dateRange)
		mock_find_a_record.assert_called_with(event['url'])

	@mock.patch('scrapper_la_liga_oficial.scrapperLaLigaOficial.requests.post')
	@mock.patch('scrapper_la_liga_oficial.matchInfoExtractor.MatchInfoExtractor.fetch_match_info')
	@mock.patch('scrapper_la_liga_oficial.matchUpdater.MatchUpdater.create_or_update_the_match')
	@mock.patch('scrapper_la_liga_oficial.fetchingHistoryManager.FetchingHistoryManager.insert_a_new_record')
	def test_fetching_an_event(
			self,
			mock_insert_a_new_record,
			mock_create_or_update_the_match,
			mock_fetch_match_info,
			mock_requests_post,
	):
		eventUrl = 'http://www.laliga.es/includes/ajax.php?action=ver_evento_calendario';
		mock_requests_post.return_value.text = '<html></html>'
		event = {
				'url': '#1_1_1_10_8_2016'
		}
		result = self.eventsFetcher.fetch_an_event(event)
		mock_requests_post.assert_called_with(eventUrl, data={'filtro': event['url']})
		mock_insert_a_new_record.assert_called_with(event['url'])

if __name__ == '__main__':
	unittest.main()
