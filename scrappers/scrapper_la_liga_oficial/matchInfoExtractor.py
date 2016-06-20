import logging
from unidecode import unidecode
import dateutil.parser
import requests
from lxml import html

class MatchInfoExtractor:

#Extract the match score and sets its status
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

#Extracts the match date
	def extract_match_date(self,match):
		hour = match.xpath('.//span[@class="fecha left"]//span[@class="hora"]')[0].text
		if hour is not None:
			hour = hour[2:].strip(' ')
		day = match.xpath('.//span[@class="fecha left"]//span[@class="dia"]')[0].text.strip(' ')
		splittedDate = day.split("-")
		result = splittedDate[2]+"-"+splittedDate[1]+"-"+splittedDate[0]
		if hour is not None:
			result = result+"T"+hour
		return dateutil.parser.parse(result)

#Extracts the referee
	def extract_referee(self,match):
		referee = match.xpath('.//span[@class="arbitro last"]')
		if (len(referee) > 0) :
			return referee[0].text

#Extracts a match hashtag
	def extract_hashtag(self,link,matchesWithoutHashtagCounter):
		detailsPage = requests.post(link)
		detailsTree = html.fromstring(detailsPage.text)
		prehashtag = detailsTree.xpath('.//div[@id="hashtag"]')
		if len(prehashtag) > 0:
			hashtag = prehashtag[0].text
			result = (matchesWithoutHashtagCounter,hashtag)
		else: 
			result = (matchesWithoutHashtagCounter+1,None)
		return result

#Extracts a team
	def extract_team(self,match,isLocal,teamsCollection,newTeamsCounter):
		divKey = 'local' if isLocal else 'visitante'
		teamDiv = match.xpath('.//span[@class="equipo left '+divKey+'"]')
		team = teamDiv[0].xpath('.//span[@class="team"]')
		foundTeam = teamsCollection.find_one({"name" : team[0].text})
		if foundTeam is None:
			#Insert a new team
			logger = logging.getLogger("scrapperLaLigaOficial")
			logger.debug('Inserting a new team')
			snake_case = unidecode(unicode(team[0].text).lower().replace('r. ','real ').replace(' ','_').replace('.',''))
			newTeam = {'name' : team[0].text, 'tag' : snake_case}
			newTeamId = teamsCollection.insert(newTeam)
			result = (newTeamsCounter+1,newTeamId)
		else:
			result = (newTeamsCounter,foundTeam['_id'])
		return result
