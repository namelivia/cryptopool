#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import html
from lxml import etree
from lxml.etree import tostring
import requests
import json
import logging
import time
import os
from datetime import datetime 
import dateutil.parser
from pymongo import MongoClient
from bson.objectid import ObjectId
from matchInfoExtractor import MatchInfoExtractor
from mongoDataGenerator import MongoDataGenerator
from matchUpdater import MatchUpdater
from executionCounters import ExecutionCounters
import sys

class ScrapperLaLigaOficial:

#Prints the global results of the execution
	def print_results(self):
		executionCounters = ExecutionCounters()
		counters = executionCounters.get_counters()
		logger = logging.getLogger("scrapperLaLigaOficial")
		logger.info("{0} new teams added".format(counters['newTeamsCounter']))
		logger.info("{0} new matches added".format(counters['newMatchesCounter']))
		logger.info("{0} existing matches updated".format(counters['updatedMatchesCounter']))
		logger.info("{0} matches had no link".format(counters['matchesWithoutLink']))
		logger.info("{0} matches had no hashtag".format(counters['matchesWithoutHashtag']))

#Initializes the loggers
	def init_logger(self):
		stderrLogger=logging.StreamHandler()
		logging.getLogger().addHandler(stderrLogger)
		stderrLogger.setLevel(logging.INFO)
		logging.getLogger("requests").setLevel(logging.WARNING)
		logger = logging.getLogger("scrapperLaLigaOficial")
		execPath = os.path.dirname(os.path.realpath(__file__))
		handler = logging.FileHandler(execPath+"/../logs/scrapperLaLigaOficial-{0}.log".format(int(time.time())))
		logger.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		logger.addHandler(handler)
		return logger

#TODO: This is not even done! And I think this scrapper should not do it
#Updates the pending pools for the updated match
#	def update_match_pools(self,matchId, score1, score2):
#		pools = poolsCollection.find({'match_id' : matchId});
#		print(pools);
#		exit();


#Finds the data in the page
	def data_find(self, page):
		#if something breaks try changing this
		ANNOYING_LENGTH = -2
		#ANNOYING_LENGTH = -1
		tree = html.fromstring(page)
		scripts = tree.xpath('//script')
		#This is pretty ugly
		longestScriptIndex = 1
		longestScriptLength = 0
		#finds the longest script in scripts
		for key,script in enumerate(scripts):
			if script.text is not None and len(script.text) > longestScriptLength:
				longestScriptIndex = key
				longestScriptLength = len(script.text)
		#Splits the scrip in lines and finds the longest line
		longestContentIndex = 1
		longestContentLength = 0
		for key,content in enumerate(scripts[longestScriptIndex].text.split('\n')):
			if content is not None and len(content) > longestContentLength:
				longestContentIndex = key
				longestContentLength = len(content)
		#Returns the longest line of the longest script
		return scripts[longestScriptIndex].text.split('\n')[longestContentIndex][20:ANNOYING_LENGTH]

	def fetch_match_info(self, match, teamsCollection):
		matchInfoExtractor = MatchInfoExtractor()
		logger = logging.getLogger("scrapperLaLigaOficial")
		#Fetch one match
		logger.debug('Fetching a match')
		newMatch = {}

		#TODO: From here this should be moved to extract_details
		prelink = match.xpath('.//a')
		#Check if the match does not have a link
		if len(prelink) == 0:
			#TODO: Deal with this
			print('TODO!')
			#counters['matchesWithoutLink'] += 1;
			#continue?
			#return?

		#start retrieving a match info
		link = prelink[0].get('href')

		#extract the hashtag TODO: Extract details
		newMatch['hashtag'] = matchInfoExtractor.extract_hashtag(link)

		#extract the referee
		newMatch['arbitro'] = matchInfoExtractor.extract_referee(match)
		
		#extract the local team
		newMatch['player1'] = matchInfoExtractor.extract_team(match,True,teamsCollection)

		#extract the visitant team
		newMatch['player2'] = matchInfoExtractor.extract_team(match,False,teamsCollection)

		#extract the date
		newMatch['date'] = matchInfoExtractor.extract_match_date(match)

		#extract the score and the status
		(newMatch['score1'], newMatch['score2'], newMatch['status']) = matchInfoExtractor.extract_score_and_status(match)
		return newMatch

#main
	def start_scrapping(self,dateRange):
		db = MongoClient('localhost',3001).meteor
#init logging
		logger = self.init_logger()

#start scrapping
		logger.info('Scrapping the official La Liga page')
		startTime = time.time()

#load existing data
		logger.debug('Loading existing teams')
		teamsCollection = db.teams
		logger.debug('Loading exsiting matches')
		matchesCollection = db.matches
		#logger.debug('Loading exsiting pools')
		#poolsCollection = db.pools
		logger.debug('Loading already feched links')
		execPath = os.path.dirname(os.path.realpath(__file__))
		lines = tuple(open(execPath+'/../fetchedLinks', 'r'))
		lines = [line[:-1] for line in lines]

#Start fetching information
		logger.debug('Fetching information')
#Fecthing the calendar
		logger.debug('Fetching the calendar')
		page = requests.get('http://www.laliga.es/calendario-horario/')
		data = self.data_find(page.text)
		parsedData = json.loads(data)

#Start fetching the events
		logger.debug('Fetching events')
		fh = open('fetchedLinks', 'a')

		for event in parsedData :
			#check if I've already have it
			#TODO: Check the updating range time
			splittedEvents = event['url'].split('_');
			eventDate = dateutil.parser.parse(splittedEvents[5]+'-'+splittedEvents[4]+'-'+splittedEvents[3])
			delta = datetime.fromtimestamp(startTime) - eventDate
			if event['url'] in lines and dateRange is not None and abs(delta).days > dateRange:
				logger.debug('I already have the '+event['url']+' event')
				continue

			#Fetch one event
			logger.debug('Fetching an event')
			eventUrl = 'http://www.laliga.es/includes/ajax.php?action=ver_evento_calendario'
			queryData = {'filtro': event['url']}
			page = requests.post(eventUrl, data=queryData)
			tree = html.fromstring(page.text)

			#Find the matches in the event
			logger.debug('Fetching the matches')
			matches = tree.xpath('//div[contains(@class,"partido")]')[2:]

			matchUpdater = MatchUpdater()
			for idx, match in enumerate(matches):
				matchInfo = self.fetch_match_info(match, teamsCollection)

				#create or update the match
				matchUpdater.create_or_update_the_match(matchesCollection, matchInfo)
				
			#write it in the already fetched links
			fh.write(event['url']+'\n')
		fh.close()

		#print the results and exit
		self.print_results()
		endTime = time.time()
		executionTime = endTime - startTime
		logger.info("The execution took "+str(executionTime)+" seconds")
		logger.info("Done")

