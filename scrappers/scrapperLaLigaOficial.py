#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import html
from lxml import etree
from unidecode import unidecode
import requests
import json
import logging
import time
import os
from pymongo import MongoClient

#set the root path
execPath = os.path.dirname(os.path.realpath(__file__))

client = MongoClient('localhost',3001)
db = client.meteor

#init logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(execPath+"/logs/scrapperLaLigaOficial-{0}.log".format(int(time.time())))
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


#start scrapping
logger.info('Scrapping the 20 minutos page')
logger.info('Loading existing teams')
teams = db.teams
logger.info('Loading exsiting matches')
matches = db.matches
logger.info('Fetching information')
logger.debug('Fetching the calendar')
page = requests.get('http://www.laliga.es/calendario-horario/')
tree = html.fromstring(page.text)
scripts = tree.xpath('//script')
data = scripts[8].text.split('\n')[20][20:-2]
parsedData = json.loads(data)
newMatchesCounter = 0
newTeamsCounter = 0
updatedMatchesCounter = 0
logger.info('Fetching events')
for event in parsedData :
	logger.debug('Fetching an event')
	urlEvento = 'http://www.laliga.es/includes/ajax.php?action=ver_evento_calendario'
	datosPeticion = {'filtro': event['url']}
	page = requests.post(urlEvento, data=datosPeticion)
	tree = html.fromstring(page.text)
	partidos = tree.xpath('//div[contains(@class,"partido")]')[2:]
	logger.debug('Fetching the matches')
	for idx,partido in enumerate(partidos):
		logger.debug('Fetching a match')
		match = {}
		link = partido.xpath('.//a')[0].get('href')
		detailsPage = requests.post(link)
		detailsTree = html.fromstring(detailsPage.text)
		hashtag = detailsTree.xpath('.//div[@id="hashtag"]')[0].text
		fecha = partido.xpath('.//span[@class="fecha left"]')
		arbitro = partido.xpath('.//span[@class="arbitro last"]')
		localDiv = partido.xpath('.//span[@class="equipo left local"]')
		local = localDiv[0].xpath('.//span[@class="team"]')
		visitanteDiv = partido.xpath('.//span[@class="equipo left visitante"]')
		visitante = visitanteDiv[0].xpath('.//span[@class="team"]')
		horaResultadoDiv = partido.xpath('.//span[@class="hora_resultado left"]')
		horaResultado = horaResultadoDiv[0].xpath('.//span[@class="horario_partido hora"]')
		
		foundTeam = teams.find_one({"name" : local[0].text})
		if foundTeam is None:
			logger.debug('Inserting a new team')
			snake_case = unidecode(unicode(local[0].text).lower().replace('r. ','real ').replace(' ','_').replace('.',''))
			newTeam = {'name' : local[0].text, 'tag' : snake_case}
			newTeamId = teams.insert(newTeam)
			newTeamsCounter += 1
			local = newTeamId
		else:
			local = foundTeam['_id']

		foundTeam = teams.find_one({"name" : visitante[0].text})
		if foundTeam is None:
			logger.debug('Inserting a new team')
			snake_case = unidecode(unicode(visitante[0].text).lower().replace('r. ','real ').replace(' ','_').replace('.',''))
			newTeam = {'name' : visitante[0].text, 'tag' : snake_case}
			newTeamId = teams.insert(newTeam)
			newTeamsCounter += 1
			visitant = newTeamId
		else:
			visitant = foundTeam['_id']

		if (len(arbitro) > 0) :
			match['arbitro'] = arbitro[0].text
		if (len(fecha) > 0) :
			splittedDateTime = fecha[0].text[1:].split(" ")
			splittedDate = splittedDateTime[0].split("-")
			match['date'] = splittedDate[2]+"-"+splittedDate[1]+"-"+splittedDate[0]
			if len(splittedDateTime) > 1 :
				match['date'] += " "+splittedDateTime[2]+":00"
		match['player1'] = local
		match['player2'] = visitant
		match['resultadohora'] = horaResultado[0].text
		match['score1'] = horaResultado[0].text.split("-")[0]
		match['score2'] = horaResultado[0].text.split("-")[1]
		match['hashtag'] = hashtag
		if match['resultadohora'] == "-":
			match['status'] = 0
		else:
			match['status'] = 1
		foundMatch = matches.find_one({
			"player1" : match['player1'],
			"player2" : match['player2'],
			"date" : match['date'],
		})
		if foundMatch is None:
			logger.debug('Inserting a new match')
			matches.insert(match)
			newMatchesCounter += 1
		else : 
			if (foundMatch['resultadohora'] != match['resultadohora']) :
				foundMatch['resultadohora'] = match['resultadohora']
				foundMatch['score1'] = horaResultado[0].text.split("-")[0]
				foundMatch['score2'] = horaResultado[0].text.split("-")[1]
				matches.update({'_id' : foundMatch['_id']}, {"$set" : foundMatch})
				updatedMatchesCounter += 1

logger.info("{0} new teams added".format(newTeamsCounter))
logger.info("{0} new matches added".format(newMatchesCounter))
logger.info("{0} new matches updated".format(updatedMatchesCounter))
logger.info("Done")
