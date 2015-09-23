#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import html
from lxml import etree
import requests
import json
try:
	with open('../data/teams.json') as teamsFile:    
		teams = json.load(teamsFile)
except:
	print('Could not get the contents of teams.json')
	teams = []
try:
	with open('../data/matches.json') as matchesFile:    
		matches = json.load(matchesFile)
except:
	print('Could not get the contents of teams.json')
	matches = []
page = requests.get('http://www.laliga.es/calendario-horario/')
tree = html.fromstring(page.text)
scripts = tree.xpath('//script')
data = scripts[7].text.split('\n')[20][20:-2]
parsedData = json.loads(data)
newMatchesCounter = 0
newTeamsCounter = 0
print('Fetching data...')
for event in parsedData :
	urlEvento = 'http://www.laliga.es/includes/ajax.php?action=ver_evento_calendario'
	datosPeticion = {'filtro': event['url']}
	page = requests.post(urlEvento, data=datosPeticion)
	tree = html.fromstring(page.text)
	partidos = tree.xpath('//div[contains(@class,"partido")]')[2:]
	for idx,partido in enumerate(partidos):
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
			newTeam = {'id' : len(teams)+1, 'name' : local[0].text}
			teams.append(newTeam)
			newTeamsCounter += 1
			local = newTeam['id']
		else:
			local = foundTeam['id']

		foundTeam = (next((item for item in teams if item["name"] == visitante[0].text), None))
		if foundTeam is None:
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
			matches.append(match)
			newMatchesCounter += 1

print("{0} new teams added".format(newTeamsCounter))
print("{0} new matches added".format(newMatchesCounter))
with open('../data/teams.json', 'w') as outfile:
	json.dump(teams, outfile)
with open('../data/matches.json', 'w') as outfile:
	json.dump(matches, outfile)
