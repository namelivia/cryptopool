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

#TODO: Move from here?
aliases = {
	'gimnastic' : 'nastic'
}
def searchForTag(tag):
	foundTeam = dbTeams.find_one({'tag' : {'$regex' : '.*'+tag+'.*'}})
	if foundTeam is None:
		splitted = snake_case.split('_')
		for word in splitted:
			foundTeam = dbTeams.find_one({'tag' : {'$regex' : '.*'+word+'.*'}})
			if foundTeam is not None:
				return foundTeam
			else:
				foundTeam = dbTeams.find_one({'tag' : {'$regex' : '.*'+aliases[word]+'.*'}})
				return foundTeam
	else:
		return foundTeam
#set the root path
execPath = os.path.dirname(os.path.realpath(__file__))

client = MongoClient('localhost',3001)
db = client.meteor

#init logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(execPath+"/logs/scrapper20Minutos-{0}.log".format(int(time.time())))
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


#start scrapping
logger.info('Scrapping the 20 minutos page')
logger.info('Loading existing teams')
dbTeams = db.teams
players = db.players
logger.info('Fetching information')
urls = ['http://www.20minutos.es/deportes/estadisticas/liga','http://www.20minutos.es/deportes/estadisticas/liga2']
for url in urls:
	page = requests.get(url+'/teams.asp')
	tree = html.fromstring(page.text)
	teams = tree.xpath('.//table[@class="shsTable shsBorderTable"]/tr')[1:]
	newTeamsCounter = 0
	newPlayersCounter = 0
	updatedTeamsCounter = 0
	updatedPlayersCounter = 0
	logger.info('Fetching teams')
	for team in teams:
		teamId = team.xpath('.//td')[0].xpath('.//span')[0].get('class')[7:].replace('sm shs_teamLogo','')
		logger.info('Trying team id '+teamId)
		roosterPage = requests.get(url+'/rosters.asp?team='+teamId)
		roosterTree = html.fromstring(roosterPage.text)
		teamName = roosterTree.xpath('.//span[@class="countryText"]')[0].text

		#Try to find the name in the database
		logger.info('Trying to find team in the database')
		#Try the find the whole name
		snake_case = unidecode(unicode(teamName).lower().replace(' ','_').replace('.',''))
		foundTeam = searchForTag(snake_case)
		if foundTeam is None:
			print("ERROR:Team with tag: "+snake_case+" not found")
			exit()
		else :
			#If not split and try again
			print("Found team with tag: "+snake_case+" => "+foundTeam['name']+"|"+foundTeam["tag"])
			teamId = foundTeam['_id']

		rooster = roosterTree.xpath('.//table[@class="shsTable shsBorderTable"]/tr[not(@valign="bottom")]')
		logger.info('Fetching players')
		for player in rooster:
			attributes = player.xpath('.//td')
			number = attributes[0].text;
			name = attributes[1].xpath('.//a')[0].text;
			position = attributes[2].text;
			height = attributes[3].xpath('.//span')[0].text
			if height is not None:
				height = height[:-3];
			weight = attributes[4].xpath('.//span')[0].text;
			if weight is not None:
				weight = weight[:-2]	
			birthDate = attributes[5].text;
			birthCity = attributes[6].xpath('.//span')
			if len(birthCity) > 0:
				birthCity = birthCity[0].text[:-2];
				birthCountry = attributes[6].xpath('.//span/following::node()')[0];
			newPlayer = {
				'name' : name,
				'number' : number,
				'position' : position,
				'height' : height,
				'weight' : weight,
				'birthDate' : birthDate,
				'birthCity' : birthCity,
				'birthCountry' : birthCountry,
				'teamId' : teamId
			}
			players.insert(newPlayer)
logger.info("Done")
