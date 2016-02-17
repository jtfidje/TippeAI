#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Covey

# Standard libraries
import pickle
import math

# Third-party libraries

# Own libraries
import Functions as lib

data_keys = {
	"home_team":u"Start",
	"away_team":u"Rosenborg",
	"stadium":u"Sparebanken Sør Arena",
	"year":u"2015",
	"month":u"April",
	"day":u"Søndag",
	"time":u"18.00"
}

vector = lib.create_vector(data_keys)

prob = pickle.load(open("prob.pkl", "rb"))

data_res = {"H":prob["H"][len(data_keys)], "B":prob["B"][len(data_keys)], "U":prob["U"][len(data_keys)]}

for res in data_res:
	for x in range(len(vector)):
		#data_res[res] += math.log(prob[res][x][vector[x]])
		data_res[res] *= prob[res][x][vector[x]]

for k, v in data_res.items():
	print(k, v)