#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import html
from lxml import etree
import requests
import json
import logging
import time

#init logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
handler = logging.FileHandler("logs/scrapper-{0}.log".format(time.time()))
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#start scrapping
logger.info('Scrapping the official La Liga page')
logger.info('Loading existing teams')
try:
	with open('../data/teams.json') as teamsFile:    
		teams = json.load(teamsFile)
except:
	logger.warning('Could not get the contents of teams.json')
	teams = []
logger.info('Loading exsiting matches')
try:
	with open('../data/matches.json') as matchesFile:    
		matches = json.load(matchesFile)
except:
	logger.warning('Could not get the contents of teams.json')
	matches = []
logger.info('Fetching information')
logger.debug('Fetching the calendar')
page = requests.get('http://www.laliga.es/calendario-horario/')
tree = html.fromstring(page.text)
scripts = tree.xpath('//script')
data = scripts[7].text.split('\n')[20][20:-2]
parsedData = json.loads(data)
newMatchesCounter = 0
newTeamsCounter = 0
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
		fecha = partido.xpath('.//span[@class="fecha left"]')
		arbitro = partido.xpath('.//span[@class="arbitro last"]')
		localDiv = partido.xpath('.//span[@class="equipo left local"]')
		local = localDiv[0].xpath('.//span[@class="team"]')
		visitanteDiv = partido.xpath('.//span[@class="equipo left visitante"]')
		visitante = visitanteDiv[0].xpath('.//span[@class="team"]')
		horaResultadoDiv = partido.xpath('.//span[@class="hora_resultado left"]')
		horaResultado = horaResultadoDiv[0].xpath('.//span[@class="horario_partido hora"]')

		foundTeam = (next((item for item in teams if item["name"] == local[0].text), None))
		if foundTeam is None:
			logger.debug('Inserting a new team')
			newTeam = {'id' : len(teams)+1, 'name' : local[0].text}
			teams.append(newTeam)
			newTeamsCounter += 1
			local = newTeam['id']
		else:
			local = foundTeam['id']

		foundTeam = (next((item for item in teams if item["name"] == visitante[0].text), None))
		if foundTeam is None:
			logger.debug('Inserting a new team')
			newTeam = {'id' : len(teams)+1, 'name' : visitante[0].text}
			teams.append(newTeam)
			newTeamsCounter += 1
			visitant = newTeam['id']
		else:
			visitant = foundTeam['id']

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
		duplicated = False
		for item in matches :
			if (item['player1'] == match['player1'] and item['player2'] == match['player2'] and item['date'] == match['date']) :
				duplicated = True
		if not duplicated :
			logger.debug('Inserting a new match')
			matches.append(match)
			newMatchesCounter += 1

logger.info("{0} new teams added".format(newTeamsCounter))
logger.info("{0} new matches added".format(newMatchesCounter))
logger.info("Writing the teams file")
try:
	with open('../data/teams.json', 'w') as outfile:
		json.dump(teams, outfile)
except:
	logger.error('Could not write the teams file',exc_info=True)
logger.info("Writing the matches file")
try:
	with open('../data/matches.json', 'w') as outfile:
		json.dump(matches, outfile)
except:
	logger.error('Could not write the matches file',exc_info=True)
logger.info("Done")
