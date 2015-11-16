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
handler = logging.FileHandler(execPath+"/logs/scrapper20Minutos-{0}.log".format(int(time.time())))
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


#start scrapping
logger.info('Scrapping the 20 minutos page')
logger.info('Loading the teams map')
teamsMap = json.load(open('teamsMap.json'))
logger.info('Loading existing teams')
teams = db.teams
logger.info('Loading exsiting matches')
matches = db.matches
logger.info('Fetching information')
logger.debug('Fetching the team list')
page = requests.get('http://www.20minutos.es/deportes/estadisticas/liga/teams.asp')
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
	roosterPage = requests.get('http://www.20minutos.es/deportes/estadisticas/liga/rosters.asp?team='+teamId)
	roosterTree = html.fromstring(roosterPage.text)
	teamName = roosterTree.xpath('.//span[@class="countryText"]')[0].text
	snake_case = unidecode(unicode(teamName).lower().replace(' ','_').replace('.',''))
	rooster = roosterTree.xpath('.//table[@class="shsTable shsBorderTable"]/tr[not(@valign="bottom")]')
	for player in rooster:
		attributes = player.xpath('.//td')
		number = attributes[0].text;
		name = attributes[1].xpath('.//a')[0].text;
		position = attributes[2].text;
		height = attributes[3].xpath('.//span')[0].text[:-3];
		weight = attributes[4].xpath('.//span')[0].text[:-2];
		birthDate = attributes[5].text;
		birthCity = attributes[6].xpath('.//span')[0].text[:-2];
		birthCountry = attributes[6].xpath('.//span/following::node()')[0];
		print ("Number:"+number);
		print ("Name:"+name);
		print ("Position:"+position);
		print ("Height:"+height);
		print ("Weight:"+weight);
		print ("birthDate:"+birthDate);
		print ("birthCity:"+birthCity);
		print ("birthCountry:"+birthCountry);
	exit()
logger.info("Done")
