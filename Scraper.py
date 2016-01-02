#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Covey

# Standard libraries
import datetime
import sys
import re
import json

# Own libraries
from DB import DB
import Extractor as ext

''' -------------------------------------------------- '''
#	This function will print the tournament ids and	 #
#	season ids. This for informational purposes      #
''' -------------------------------------------------- '''
def print_seasons():
	# Tournament IDs
	tippeliga_id = 1
	print 'Tippeligaen --> {0}'.format(tippeliga_id)

	print '\n---\n'

	# Season IDs
	year = 2001
	season_id = 323
	print 'Year --> ID'
	for i in range(323, 337 + 1):
		print '{0} --> {1}'.format(year, season_id)
		year += 1
		season_id += 1

''' -------------------------------------------------- '''
#	This function will connect to the given tournament   #
#	and season site and look for new matches not 		 #
#	contained in the database. If new matches are 		 #
#	found, data will be extracted and saved to the db 	 #
''' -------------------------------------------------- '''
def check_for_new_matches(tournament_id, season_id):
	db = DB()

	print "Reading tournament website..."
	
	tournamenturl = 'elementsCommonAjax.do?cmd=fixturesContent&tournamentId={0}&seasonId={1}&month=all&useFullUrl=false'.format(tournament_id, season_id)

	data = ext.get_data(None, tournamenturl)

	# Extract all matches from site
	datalist = [i for i in re.findall('<a href.*class="sd_fixtures_score">.*?<', data)]

	# Remove all unplayed matches
	datalist[:] = [i for i in datalist if '&nbsp;-&nbsp;' in i]

	# Extract URLs to played matches
	datalist[:] = [i[i.index('element.do'):i.index('" class')] for i in datalist]

	print 'Checking for new played matches'

	match_ids = db.get_match_ids()
	
	match_link_list = [i for i in datalist if i[i.index('matchId')+8:i.index('&amp;tournamentId')] not in match_ids]

	if match_link_list: 
		print 'New matches found! Processing...'

		# Change '&amp;' in URLs to '&'
		match_link_list[:] = [re.sub('&amp;', '&', i) for i in match_link_list]

		for link in match_link_list:
			db_contents = db.get_all()

			match_data = extract_new_match_data(link)

			if match_data['time'] not in db_contents['times']: db.insert_new_time(match_data['time'])	
			if match_data['day'] not in db_contents['days']: db.insert_new_day(match_data['day'])
			if match_data['month'] not in db_contents['months']: db.insert_new_month(match_data['month'])
			if match_data['year'] not in db_contents['years']: db.insert_new_year(match_data['year'])
			if match_data['stadium'] not in db_contents['stadiums']: db.insert_new_stadium(match_data['stadium'])
			if match_data['home_team'] not in db_contents['teams']: db.insert_new_team(match_data['home_team'])
			if match_data['away_team'] not in db_contents['teams']: db.insert_new_team(match_data['away_team'])
			if match_data['result'] not in db_contents['results']: db.insert_new_result(match_data['result'])
			
			db.insert_new_match(match_data)

			print '\n', '-----', '\n'

		print 'All done!'
	else:
		print 'No new matches found!'

	db.close_connection()

''' -------------------------------------------------- '''
#	This function will connect to the given url and 	 #
#	extract the wanted data using regular expressions 	 #
''' -------------------------------------------------- '''
def extract_new_match_data(link):
	data = ext.get_data(None, link)

	home_team, away_team = ext.get_team_names(data)
	stadium = ext.get_stadium_name(data)
	day, month, year, time = ext.get_date_and_time(data)
	result = ext.get_results(data)
	#home_team_players, away_team_players = ext.get_players(data)
	#home_team_formation, away_team_formation = ext.get_formations(data)
	
	#--------------------------------------#
	#        Write results to file         #
	#--------------------------------------#
	print 'Extractions done! Generating dictionary and saving!'

	match_id = link[link.index('matchId')+8:link.index('&tournamentId')]

	results = {	'id':match_id,
				'day':day, 
				'month':month, 
				'year':year,
				'time':time,
				'stadium':stadium,
				'home_team':home_team,
				'away_team':away_team,
				'result':result
				#'home_team_formation':home_team_formation,
				#'home_team_players':json.dumps([player for player in home_team_players]),
				#'away_team_formation':away_team_formation,
				#'away_team_players':json.dumps([player for player in away_team_players]),
			}
	return results

def complete_download():
	year = 2001
	for i in range(323, 337 + 1):
		print 'Downloading Tippeliga-matches from', year
		year += 1

		check_for_new_matches('1', str(i))

def extract_unplayed_match(url):
	data = ext.get_data(url, None)

	day, month, year, time = ext.get_date_and_time(data)
	stadium = ext.get_stadium_name(data)
	home_team, away_team = ext.get_team_names(data)

	results = { 'day':day, 
				'month':month, 
				'year':year,
				'time':time,
				'stadium':stadium,
				'home_team':home_team,
				'away_team':away_team
				}

	return results
