from lxml import html
from lxml import etree
import dateutil.parser
from datetime import datetime 
import logging
import time
import requests
from matchInfoExtractor import MatchInfoExtractor
from matchUpdater import MatchUpdater
from fetchingHistoryManager import FetchingHistoryManager

class EventsFetcher:

	def __init__(self):
		self.matchInfoExtractor = MatchInfoExtractor()
		self.matchUpdater = MatchUpdater()
		self.fetchingHistoryManager = FetchingHistoryManager()
		self.logger = logging.getLogger("scrapperLaLigaOficial")

	def check_if_an_event_has_already_been_fetched(self, event, dateRange):
		splittedEventUrl = event['url'].split('_');
		eventDate = dateutil.parser.parse(splittedEventUrl[5]+'-'+splittedEventUrl[4]+'-'+splittedEventUrl[3])
		delta = datetime.fromtimestamp(time.time()) - eventDate
		if self.fetchingHistoryManager.find_a_record(event['url']) is not None and dateRange is not None and abs(delta).days > dateRange:
			self.logger.debug('I already have the '+event['url']+' event')
			return True
		return False

	def fetch_an_event(self, event):
		self.logger.debug('Fetching an event')
		eventUrl = 'http://www.laliga.es/includes/ajax.php?action=ver_evento_calendario'
		queryData = {'filtro': event['url']}
		page = requests.post(eventUrl, data=queryData)
		tree = html.fromstring(page.text)

		self.logger.debug('Fetching the matches')
		matches = tree.xpath('//div[contains(@class,"partido")]')[2:]

		for idx, match in enumerate(matches):
			matchInfo = self.matchInfoExtractor.fetch_match_info(match)
			if (matchInfo is not None) :
				self.matchUpdater.create_or_update_the_match(matchInfo)

		self.fetchingHistoryManager.insert_a_new_record(event['url'])
