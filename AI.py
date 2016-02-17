#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Covey

# Standard libraries
import pickle
import math

# Third-party libraries

# Own libraries
import Scraper
import Functions as func
import Extractor as ext

data_keys = {
	"home_team":u"Start",
	"away_team":u"Rosenborg",
	"stadium":u"Sparebanken Sør Arena",
	"year":u"2015",
	"month":u"April",
	"day":u"Søndag",
	"time":u"18.00"
}

prob = pickle.load(open("prob.pkl", "rb"))

data_res = {"H":prob["H"]['prior'], "B":prob["B"]['prior'], "U":prob["U"]['prior']}

for res in data_res:
	for k, v in data_keys.items():
		data_res[res] += math.log(prob[res][k][v])

for k, v in data_res.items():
	print k, v