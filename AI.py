#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Covey

# Standard libraries
import pickle
import json
import sys
import math

# Third-party libraries

# Own libraries
import Library as lib

# Load test data
db_data = json.load(open('match.json'))
test_data = db_data[3000:]

# Feature vars....
result_lst = lib.result_lst
result_len = len(result_lst)

team_lst = lib.team_lst
team_len = len(team_lst)

feature_lst = lib.feature_lst
feature_len = len(feature_lst)

# Load probabilities from file
f = open('probabilities.pkl', 'rb')
probabilities = pickle.load(f)
feature_prob = probabilities['feature_prob']
team_prob = probabilities['team_prob']
priors = probabilities['priors']
f.close()

correct = [0, 0]

# Init. confusion matrix
confusion_matrix = {x:{y:0 for y in result_lst} for x in result_lst}

for data in test_data:
	answer = data.pop('result')

	max_res = None
	max_p = 1

	teams, vector = lib.create_vector(data)

	for res in result_lst:
		p = priors[res]
		try:
			# Loop through the "team given result" probabilities
			for x in range(len(teams)):
				# Add probability of team given result
				p += math.log(team_prob[res][team_lst[x]][teams[x]])

			# Loop through the "feature given team given res" probabilities
			for x in range(len(teams)):
				for y in range(len(vector)):
					# Add probability of feature given team given res
					p += math.log(feature_prob[res][teams[x]][team_lst[x]][feature_lst[y]][vector[y]])
		except KeyError as e:
			print("Error: 1")
			continue

		# Check which P is highest
		if p >= max_p or max_p == 1:
			max_p = p
			max_res = res
	try:
		# Update confusion matrix
		confusion_matrix[answer][max_res] += 1
	
		if max_res == answer:
			correct[0] += 1
		else:
			correct[1] += 1
	except:
		print("Error: 2")
		continue


# Print the confusion matrix in a table
lib.print_results(confusion_matrix, correct)
