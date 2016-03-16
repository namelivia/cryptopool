#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import html
from lxml import etree
from lxml.etree import tostring
from unidecode import unidecode
import requests
import json
import logging
import time
import os
from datetime import datetime 
import dateutil.parser
from pymongo import MongoClient
from bson.objectid import ObjectId

#Prints the global results of the execution
def print_results(newTeamsCounter,newMatchesCounter,updatedMatchesCounter,matchesWithoutLink,matchesWithoutHashtag):
	logger = logging.getLogger("scrapperLaLigaOficial")
	logger.info("{0} new teams added".format(newTeamsCounter))
	logger.info("{0} new matches added".format(newMatchesCounter))
	logger.info("{0} existing matches updated".format(updatedMatchesCounter))
	logger.info("{0} matches had no link".format(matchesWithoutLink))
	logger.info("{0} matches had no hashtag".format(matchesWithoutHashtag))

#Initializes the loggers
def init_logger():
	stderrLogger=logging.StreamHandler()
	logging.getLogger().addHandler(stderrLogger)
	stderrLogger.setLevel(logging.INFO)
	logging.getLogger("requests").setLevel(logging.WARNING)
	logger = logging.getLogger("scrapperLaLigaOficial")
	execPath = os.path.dirname(os.path.realpath(__file__))
	handler = logging.FileHandler(execPath+"/logs/scrapperLaLigaOficial-{0}.log".format(int(time.time())))
	logger.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	return logger

#Insert a new match in the database
def insert_a_new_match(matches,match,newMatchesCounter):
	matches.insert(match)
	return newMatchesCounter + 1

#Update the match if needed
def update_match_if_needed(matches,foundMatch,match,updatedMatchesCounter,horaResultado):
	if (foundMatch['score1'] == match['score1'] and foundMatch['score2'] == match['score2']) :
		return updatedMatchesCounter
	foundMatch['score1'] = horaResultado[0].text.split("-")[0]
	foundMatch['score2'] = horaResultado[0].text.split("-")[1]
	matches.update({'_id' : foundMatch['_id']}, {"$set" : foundMatch})
	return updatedMatchesCounter + 1

#Extracts the match date
def extract_match_date(match):
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
def extract_the_referee(match):
	referee = match.xpath('.//span[@class="arbitro last"]')
	if (len(referee) > 0) :
		return referee[0].text

#main
def main():

#if something breaks try changing this
	ANNOYING_LENGTH = -2
#ANNOYING_LENGTH = -1
	db = MongoClient('localhost',3001).meteor
#init logging
	logger = init_logger()

#start scrapping
	logger.info('Scrapping the official La Liga page')

#load existing data
	logger.debug('Loading existing teams')
	teams = db.teams
	logger.debug('Loading exsiting matches')
	matches = db.matches
	logger.debug('Loading already feched links')
	lines = tuple(open('fetchedLinks', 'r'))
	lines = [line[:-1] for line in lines]
#Initializing counters
	newMatchesCounter = 0
	newTeamsCounter = 0
	updatedMatchesCounter = 0
	matchesWithoutHashtag = 0
	matchesWithoutLink = 0;

#Start fetching information
	logger.debug('Fetching information')
#Fecthing the calendar
	logger.debug('Fetching the calendar')
	page = requests.get('http://www.laliga.es/calendario-horario/')
	tree = html.fromstring(page.text)
	scripts = tree.xpath('//script')
	#Ugly!
	longestScriptIndex = 8
	for key,script in enumerate(scripts):
		if script.text is not None and len(script.text) > 1000:
			longestScriptIndex = key
	for key,content in enumerate(scripts[longestScriptIndex].text.split('\n')):
		if content is not None and len(content) > 10000:
			longestContentIndex = key
	data = scripts[longestScriptIndex].text.split('\n')[longestContentIndex][20:ANNOYING_LENGTH]
	parsedData = json.loads(data)

#Start fetching the events
	logger.debug('Fetching events')
	fh = open('fetchedLinks', 'a')

	for event in parsedData :
		#check if I've already have it
		if event['url'] in lines and int(event['url'].split('_')[5]) != datetime.now().year:
			logger.debug('I already have the '+event['url']+' event')
			continue

		#Fetch one event
		logger.debug('Fetching an event')
		urlEvento = 'http://www.laliga.es/includes/ajax.php?action=ver_evento_calendario'
		datosPeticion = {'filtro': event['url']}
		page = requests.post(urlEvento, data=datosPeticion)
		tree = html.fromstring(page.text)

		#Find the matches in the event
		logger.debug('Fetching the matches')
		partidos = tree.xpath('//div[contains(@class,"partido")]')[2:]

		for idx,partido in enumerate(partidos):
			#Fetch one match
			logger.debug('Fetching a match')
			prelink = partido.xpath('.//a')
			#Check if the match does not have a link
			if len(prelink) == 0:
				matchesWithoutLink += 1;
				continue

			#start retrieving a match info
			match = {}
			link = prelink[0].get('href')
			detailsPage = requests.post(link)
			detailsTree = html.fromstring(detailsPage.text)

			#get the hastag
			prehashtag = detailsTree.xpath('.//div[@id="hashtag"]')
			if len(prehashtag) > 0:
				hashtag = prehashtag[0].text
			else: 
				matchesWithoutHashtag += 1;
			match['hashtag'] = hashtag

			#set the referee
			match['arbitro'] = extract_the_referee(partido)
			
			#try to locate the local team
			localDiv = partido.xpath('.//span[@class="equipo left local"]')
			local = localDiv[0].xpath('.//span[@class="team"]')
			foundTeam = teams.find_one({"name" : local[0].text})
			if foundTeam is None:
				#Insert a new team
				logger.debug('Inserting a new team')
				snake_case = unidecode(unicode(local[0].text).lower().replace('r. ','real ').replace(' ','_').replace('.',''))
				newTeam = {'name' : local[0].text, 'tag' : snake_case}
				newTeamId = teams.insert(newTeam)
				newTeamsCounter += 1
				local = newTeamId
			else:
				local = foundTeam['_id']
			match['player1'] = local

			#try to locate the visitant team
			visitanteDiv = partido.xpath('.//span[@class="equipo left visitante"]')
			visitante = visitanteDiv[0].xpath('.//span[@class="team"]')
			foundTeam = teams.find_one({"name" : visitante[0].text})
			if foundTeam is None:
				#Insert a new team
				logger.debug('Inserting a new team')
				snake_case = unidecode(unicode(visitante[0].text).lower().replace('r. ','real ').replace(' ','_').replace('.',''))
				newTeam = {'name' : visitante[0].text, 'tag' : snake_case}
				newTeamId = teams.insert(newTeam)
				newTeamsCounter += 1
				visitant = newTeamId
			else:
				visitant = foundTeam['_id']
			match['player2'] = visitant

			#process the date
			match['date'] = extract_match_date(partido)

			#process the score
			horaResultadoDiv = partido.xpath('.//span[@class="hora-resultado left"]')
			horaResultado = horaResultadoDiv[0].xpath('.//span[@class="horario-partido hora"]')
			match['score1'] = horaResultado[0].text.split("-")[0]
			match['score2'] = horaResultado[0].text.split("-")[1]
			if match['score1'] == "" and match['score2'] == "":
				match['status'] = 0
			else:
				match['status'] = 1

			#Try to find if the match is already in the database, and has to be updated or inserted	
			foundMatch = matches.find_one({
				"player1" : ObjectId(match['player1']),
				"player2" : ObjectId(match['player2']),
				"date" : match['date'],
			})
			if foundMatch is None:
				logger.debug('Inserting a new match')
				logger.debug(match)
				newMatchesCounter = insert_a_new_match(matches,match,newMatchesCounter)
			else : 
				logger.debug('Updating an existing match if needed')
				updatedMatchesCounter = update_match_if_needed(matches,foundMatch,match,updatedMatchesCounter,horaResultado)
			
		#write it in the already fetched links
		fh.write(event['url']+'\n')
	fh.close()

	#print the results and exit
	print_results(newTeamsCounter,newMatchesCounter,updatedMatchesCounter,matchesWithoutLink,matchesWithoutHashtag)
	logger.info("Done")


if __name__ == "__main__":
	main()
