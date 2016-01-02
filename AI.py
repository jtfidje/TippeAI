#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Covey

# Standard libraries
import pickle

# Third-party libraries

# Own libraries
from DB import DB
import Scraper
import Functions as func
import Extractor as ext

db = DB()

match_data = list()
matches = [list(x) for x in db.get_all_matches()]

for match in matches:
	result = match.pop(-1)
	match_data.append([match, result])

training_data, test_data = match_data[:3100], match_data[3100:] 

data = (func.create_data_tuple(training_data),
		func.create_data_tuple(test_data),
		func.create_data_tuple(test_data)
		)

f = open('data.pkl', 'wb')
pickle.dump(data, f)
f.close()
