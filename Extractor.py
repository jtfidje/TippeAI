#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Covey

# Standard libraries
import re
import datetime

# Third-party libraries
import mechanize

# Own libraries

#--------------------------------------#
#             Read website             #
#--------------------------------------#
def get_data(url = None, link = None):
	baseurl = 'http://www.altomfotball.no/'

	# Make a Mech.Browser
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	browser.set_handle_refresh(False)
	if url:
		browser.open(url)
	elif link:
		browser.open(baseurl + link)

	data = browser.response().read()

	return data

#--------------------------------------#
#       Get list of all players        #
#--------------------------------------#
def get_players(data):
	print 'Extracting playernames'
	datalist = [i for i in re.findall('homePlayers".*?</table', data, re.S)]
	datalist = re.findall('">(.*?)&nbsp?', datalist[0])
	home_team_players = [i for i in datalist]


	datalist = re.findall('awayPlayers".*?</table', data, re.S)
	datalist = re.findall('">(.*?)&nbsp?', datalist[0])
	away_team_players = [i for i in datalist]

	return home_team_players, away_team_players

#--------------------------------------#
#            Get formations            #
#--------------------------------------#
def get_formations(data):
	print 'Extracting formations'
	home_team_formation = re.findall('formationHomeTeam.*&nbsp;(.*)?</div>', data)[0]
	away_team_formation = re.findall('formationAwayTeam.*&nbsp;(.*)?</div>', data)[0]

	return home_team_formation, away_team_formation

#--------------------------------------#
#            Get team names            #
#--------------------------------------#
def get_team_names(data):
	print 'Extracting team names'
	home_team, away_team = [i for i in re.findall('<img.*laglogo.*/>(.*)</a', data)]

	return home_team, away_team
	
#--------------------------------------#
#          Get date and time           #
#--------------------------------------#
def get_date_and_time(data):
	print 'Extracting date and time'
	weekdays = {0:'Mandag', 1:'Tirsdag', 2:'Onsdag', 3:'Torsdag', 4:'Fredag', 5:'Lørdag', 6:'Søndag'}
	months = {'01':'Januar', '02':'Februar', '03':'Mars', '04':'April', '05':'Mai', '06':'Juni', '07':'Juli', '08':'August', '09':'September', '10':'Oktober', '11':'November', '12':'Desember'}

	day, month, year = re.findall('sd_game_away.*(\d\d)\.(\d\d)\.(\d\d\d\d)', data, re.S)[0]

	day = weekdays[datetime.date(int(year), int(month), int(day)).weekday()]
	month = months[month]
	time = re.findall('sd_game_away.*kl\.\s(\d\d\.\d\d)', data, re.S)[0]

	return day, month, year, time

#--------------------------------------#
#           Get stadium name           #
#--------------------------------------#
def get_stadium_name(data):
	print 'Extracting stadium name'
	stadium = re.findall('sd_match_details.*<h3>(.*),.*</h3>', data, re.S)[0]

	return stadium

#--------------------------------------#
#             Get results              #
#--------------------------------------#
def get_results(data):
	print 'Extracting results'
	numRes = ''.join(re.findall('sd_game_score.*(\d\D\d)</td>', data, re.S)).split('-')
	if(int(numRes[0]) > int(numRes[1])):
		result = 'H'
	elif(int(numRes[0]) < int(numRes[1])):
		result = 'B'
	else:
		result = 'U'

	return result

#--------------------------------------#
#         Get table placement          #
#--------------------------------------#
def get_table_placement(team):
	print 'Extracting table placement for {0}'.format(team)
	url = 'http://www.altomfotball.no/element.do?cmd=tournamentTable&tournamentId=1&seasonId=337&useFullUrl=false'
	data = get_data(url, None)

	placement = re.findall('sd_table_new.*>([0-9]{1,2}).*' + team + '?', data, re.S)

	return float(placement[0])

