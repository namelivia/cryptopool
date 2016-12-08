#!/usr/bin/python
# -*- coding: utf-8 -*-
from lxml import html
from lxml import etree
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
handler = logging.FileHandler(execPath+"/logs/scrapperLogos-{0}.log".format(int(time.time())))
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


#start scrapping
logger.info('Scrapping the team logos')
urls = ['http://lafutbolteca.com/primera/','http://lafutbolteca.com/segundaa/']
logosFetched = 0
for url in urls :
	page = requests.get(url)
	tree = html.fromstring(page.text)
	images = tree.xpath('//img[contains(@class,"size-thumbnail")]')
	for image in images :
		filename = image.attrib['title'].lower().replace(' ','_')
		with open('../meteorApp/public/logos/'+filename+'.jpg', 'wb') as outf:
			data = requests.get(image.attrib['src']).content
			outf.write(data)
		logosFetched += 1
logger.info("{0} logos downloaded".format(logosFetched))
logger.info("Done")
