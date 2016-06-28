#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import html
from lxml import etree
import requests
import json
import logging
import time
import os
from executionCounters import ExecutionCounters
from eventsFetcher import EventsFetcher

class ScrapperLaLigaOficial:
	def __init__(self):
		self.executionCounters = ExecutionCounters()
		self.eventsFetcher = EventsFetcher()

	def print_results(self, executionTime):
		counters = self.executionCounters.get_counters()
		logger = logging.getLogger("scrapperLaLigaOficial")
		logger.info("{0} new teams added".format(counters['newTeamsCounter']))
		logger.info("{0} new matches added".format(counters['newMatchesCounter']))
		logger.info("{0} existing matches updated".format(counters['updatedMatchesCounter']))
		logger.info("{0} matches had no link".format(counters['matchesWithoutLink']))
		logger.info("{0} matches had no hashtag".format(counters['matchesWithoutHashtag']))
		logger.info("The execution took "+str(executionTime)+" seconds")
		logger.info("Done")

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
		#Splits the script in lines and finds the longest line
		longestContentIndex = 1
		longestContentLength = 0
		for key,content in enumerate(scripts[longestScriptIndex].text.split('\n')):
			if content is not None and len(content) > longestContentLength:
				longestContentIndex = key
				longestContentLength = len(content)
		#Returns the longest line of the longest script
		return scripts[longestScriptIndex].text.split('\n')[longestContentIndex][20:ANNOYING_LENGTH]

	def start_scrapping(self,dateRange):

		logger = self.init_logger()
		logger.info('Scrapping the official La Liga page')
		startTime = time.time()
		page = requests.get('http://www.laliga.es/calendario-horario/')
		data = self.data_find(page.text)
		parsedData = json.loads(data)
		for event in parsedData :
			logger.debug('Fetching an event:'+event['url'])
			if(not self.eventsFetcher.check_if_an_event_has_already_been_fetched(event, dateRange)):
				self.eventsFetcher.fetch_an_event(event)

		executionTime = time.time() - startTime
		self.print_results(executionTime)

