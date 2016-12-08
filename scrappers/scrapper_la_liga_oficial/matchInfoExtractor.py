import logging
import pprint
from unidecode import unidecode
import dateutil.parser
import requests
from lxml import html
from executionCounters import ExecutionCounters
from teamsCollectionManager import TeamsCollectionManager

class MatchInfoExtractor:
	def __init__(self):
		self.executionCounters = ExecutionCounters()
		self.teamsCollectionManager = TeamsCollectionManager()
		self.logger = logging.getLogger("scrapperLaLigaOficial")

	def fetch_match_info(self, match, competitionId):
		newMatch = {}

		#TODO: From here this should be moved to extract_details
		prelink = match.xpath('.//a')
		if len(prelink) == 0:
			self.logger.debug('The match has no link and cant be fetched')
			self.executionCounters.increase_matches_without_link_counter()
			return

		link = prelink[0].get('href')
		newMatch['competition_id'] = competitionId
		newMatch['hashtag'] = self.extract_hashtag(link)
		newMatch['referee'] = self.extract_referee(match)
		newMatch['player1'] = self.extract_local_team(match)
		newMatch['player2'] = self.extract_visitant_team(match)
		newMatch['date'] = self.extract_match_date(match)
		(newMatch['score1'], newMatch['score2'], newMatch['status']) = self.extract_score_and_status(match)
		return newMatch

	def extract_local_team(self, match):
		return self.extract_team(match, True)

	def extract_visitant_team(self, match):
		return self.extract_team(match, False)

	def extract_score_and_status(self,match):
		result = {}
		horaResultadoDiv = match.xpath('.//span[@class="hora-resultado left"]')
		horaResultado = horaResultadoDiv[0].xpath('.//span[@class="horario-partido hora"]')
		result['score1'] = horaResultado[0].text.split("-")[0]
		result['score2'] = horaResultado[0].text.split("-")[1]
		if result['score1'] == "" and result['score2'] == "":
			result['status'] = 0
		else:
			result['status'] = 1
		return (result['score1'], result['score2'], result['status'])

	def extract_match_date(self,match):
		date = match.xpath('.//span[@class="fecha left"]')[0]
		day = date.xpath('.//span[@class="dia"]')
		if (len(day) > 0):
			splittedDate = day[0].text.strip(' ').split("-")
			result = splittedDate[2]+"-"+splittedDate[1]+"-"+splittedDate[0]
			hour = date.xpath('.//span[@class="hora"]')[0].text
			if hour is not None:
				hour = hour[2:].strip(' ')
			if hour is not None:
				result = result+"T"+hour
			return dateutil.parser.parse(result)

	def extract_referee(self,match):
		referee = match.xpath('.//span[@class="arbitro last"]')
		if (len(referee) > 0) :
			return referee[0].text

	def extract_hashtag(self,link):
		detailsPage = requests.post(link)
		detailsTree = html.fromstring(detailsPage.text)
		prehashtag = detailsTree.xpath('.//div[@id="hashtag"]')
		if len(prehashtag) > 0:
			return prehashtag[0].text
		else: 
			self.executionCounters.increase_matches_without_hashtag_counter()

	def extract_team(self,match,isLocal):
		divKey = 'local' if isLocal else 'visitante'
		teamDiv = match.xpath('.//span[@class="equipo left '+divKey+'"]')
		team = teamDiv[0].xpath('.//span[@class="team"]')
		foundTeam = self.teamsCollectionManager.find_a_team_by_name(team[0].text)
		if foundTeam is None:
			self.logger.debug('Inserting a new team')
			snake_case = unidecode(unicode(team[0].text).lower().replace('r. ','real ').replace(' ','_').replace('.',''))
			newTeam = {'name' : team[0].text, 'tag' : snake_case}
			self.logger.debug(pprint.pformat(newTeam))
			newTeamId = self.teamsCollectionManager.insert_a_new_team(newTeam)
			self.executionCounters.increase_new_teams_counter()
			return newTeamId
		else:
			return foundTeam['_id']
		return result
