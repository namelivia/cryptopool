from lxml import html
from lxml import etree
import dateutil.parser
from datetime import datetime 
import logging
import time
import requests
from executionCounters import ExecutionCounters
from matchInfoExtractor import MatchInfoExtractor
from matchUpdater import MatchUpdater
from competitionsCollectionManager import CompetitionsCollectionManager
from fetchingHistoryManager import FetchingHistoryManager

class EventsFetcher:

	def __init__(self):
		self.matchInfoExtractor = MatchInfoExtractor()
		self.matchUpdater = MatchUpdater()
		self.executionCounters = ExecutionCounters()
		self.competitionsCollectionManager = CompetitionsCollectionManager()
		self.fetchingHistoryManager = FetchingHistoryManager()
		self.logger = logging.getLogger("scrapperLaLigaOficial")

	def check_if_an_event_has_already_been_fetched(self, event, dateRange):
		splittedEventUrl = event['url'].split('_');
		eventDate = dateutil.parser.parse(splittedEventUrl[5]+'-'+splittedEventUrl[4]+'-'+splittedEventUrl[3])
		delta = datetime.fromtimestamp(time.time()) - eventDate
		if self.fetchingHistoryManager.find_a_record(event['url']) is not None and dateRange is not None and abs(delta).days > dateRange:
			self.logger.debug('The event was already scrapped so it will be skipped')
			return True
		return False

	def fetch_an_event(self, event):
		eventUrl = 'http://www.laliga.es/includes/ajax.php?action=ver_evento_calendario'
		queryData = {'filtro': event['url']}
		page = requests.post(eventUrl, data=queryData)
		tree = html.fromstring(page.text)
		competitionId = self.fetch_the_competition_for_an_event(tree, event['url'])
		self.logger.debug('Fetching the event content')
		matches = tree.xpath('//div[contains(@class,"partido")]')[2:]

		for idx, match in enumerate(matches):
			self.logger.debug('Trying to fetch a match')
			matchInfo = self.matchInfoExtractor.fetch_match_info(match,competitionId)
			if (matchInfo is not None) :
				self.matchUpdater.create_or_update_the_match(matchInfo)

		self.fetchingHistoryManager.insert_a_new_record(event['url'])

	def fetch_the_competition_for_an_event(self, tree, eventUrl):
		header = tree.xpath('//td[@id="titulo-jornada"]')
		if (len(header) > 0):
			code = header[0].get('class')[18:]
			competition = self.competitionsCollectionManager.find_a_competition(code)
			if competition is None:
				self.logger.debug('This competition is new so I will create it')
				newCompetition = {
						'code' : code,
						#TODO: There is no way to determine the competition name, so
						#provisionally I will store the event url to check it manually
						'name' : 'event'+eventUrl
				}
				self.executionCounters.increase_new_competitions_counter()
				return self.competitionsCollectionManager.insert_a_new_competition(newCompetition)
			else:
				return competition['_id']
		else:
			self.logger.debug('This event has no competition code')
