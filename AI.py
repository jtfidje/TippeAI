#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Covey

# Standard libraries
import sys
import pickle
import math

# Third-party libraries

# Own libraries
import Library as lib

result_lst = lib.result_lst
result_len = len(result_lst)

team_lst = lib.team_lst
team_len = len(team_lst)

feature_lst = lib.feature_lst
feature_len = len(feature_lst)

data_keys = {
	'home_team':u'Aalesund',
	'away_team':u'Start',
	'stadium':u'Color Line Stadion',
	'year':u'2015',
	'month':u'Mars',
	'day':u'Fredag',
	'time':u'18.00'
}

teams, vector = lib.create_vector(data_keys)

feature_prob = pickle.load(open('feature_prob.pkl', 'rb'))
team_prob = pickle.load(open('team_prob.pkl', 'rb'))
priors = pickle.load(open('priors.pkl', 'rb'))

data_res = {'H':priors['H'], 'B':priors['B'], 'U':priors['U']}

for res in result_lst:
	for x in range(len(teams)):
		#data_res[res] *= team_prob[res][x][teams[x]]
		data_res[res] += math.log(team_prob[res][team_lst[x]][teams[x]])

		for y in range(len(vector)):
				#data_res[res] *= feature_prob[res][teams[x]][team_lst[x]][feature_lst[y]][vector[y]]
				data_res[res] += math.log(feature_prob[res][teams[x]][team_lst[x]][feature_lst[y]][vector[y]])

print(sorted(data_res.items(), key = lambda x:x[1], reverse = True))