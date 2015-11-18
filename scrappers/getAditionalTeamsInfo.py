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
	'gimnastic' : 'nastic',
}

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
logger.info('Getting aditional teams info')
logger.info('Loading existing teams')
dbTeams = db.teams
logger.info('Fetching information')
#urls = ['http://www.20minutos.es/deportes/estadisticas/liga','http://www.20minutos.es/deportes/estadisticas/liga2']
for team in dbTeams.find({},{"tag" : 1}):
	page = requests.get('http://laliga.es/liga-bbva/'+team['tag'].replace('_','-'))
	tree = html.fromstring(page.text)
	notFound = tree.xpath('.//div[@id="contenido_404"]')
	if (len(notFound) == 0) :
		print(team['tag']+' found');
		teamData = tree.xpath('.//div[@id="box_datos_equipo"]')[0]
		stadium = teamData.xpath('.//span[@class="datos_informativos datos_estadio"]')[0]
		if len(stadium) == 3:
			stadiumName = stadium.xpath('.//p')[0].text;
			stadiumAddress = stadium.xpath('.//p')[1].text+stadium.xpath('.//p')[2].text
		else:
			stadiumName = None
			if len(stadium) == 2:
				stadiumAddress = stadium.xpath('.//p')[0].text+stadium.xpath('.//p')[1].text
			else:
				stadiumAddress = stadium.xpath('.//p')[0].text
		website = teamData.xpath('.//div[@id="lugar_nacimiento"]')[0].xpath('.//span')[0].xpath('.//a')[0].get('href')
		twitter = teamData.xpath('.//div[@id="altura"]')[0].xpath('.//span')[0].xpath('.//a')[0].get('href')
		facebook = teamData.xpath('.//div[@id="peso"]')
		if len(facebook) > 0 :
			facebook = facebook[0].xpath('.//span')[0].xpath('.//a')[0].get('href')
		else:
			facebook = None
		email = teamData.xpath('.//div[@id="nacionalidad"]')
		if len(email) > 0 :
			email = email[0].xpath('.//span')[0].xpath('.//a')[0].get('href')
		else:
			email = None
		contact = teamData.xpath('.//div[@id="dorsal"]')[0].xpath('.//span')[0].text
		db.teams.update({"_id": team["_id"]}, {"$set": {
			"stadium": stadiumName,
			"address": stadiumAddress,
			"website": website,
			"twitter": twitter,
			"facebook": facebook,
			"email": email,
			"contact": contact
		}})
	else:
		print(team['tag']+' not found');
logger.info("Done")
