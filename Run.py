#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Covey

from DB import DB
import Scraper
import Extractor as ext

db = DB()

url = 'http://www.altomfotball.no/element.do?cmd=tournamentTable&tournamentId=1&seasonId=337&useFullUrl=false'

db.drop_collection('tippeligaen')
db.drop_collection('tippeliga')

Scraper.complete_download()
