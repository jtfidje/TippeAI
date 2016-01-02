#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Covey
""" This is a Database helper class """
import sys
import library as lib
from pymongo import MongoClient

class DB:
	def __init__(self):
		self.client = MongoClient()
		self.db = self.client['local']

	def insert(self, collection, data):
		try:
			result = self.db[collection].insert(data)
		except:
			print('Error while inserting to collection \'{0}\''.format(collection))

	def update_exists(self, collection, key, data):
		try:
			result = self.db[collection].update_one({key: {'$exists': True}}, {'$push': {key: data}}, upsert = True)
		except:
			print('Error while updating document in collection {0}'.format(collection))

	def update_key(self, collection, key, value, data):
		try:
			result = self.db[collection].update_one({key:value}, {'$push':{'data':data}}, upsert = True)
		except:
			print('Error while updating document with \'{0}:{1}\' in collection \'{2}\''.format(key, value, collection))
			
	def find_all(self, collection, timeout = True):
		try:
			if timeout:
				cursor = self.db[collection].find()
				return cursor

			cursor = self.db[collection].find(no_cursor_timeout = True)
			return cursor
		except:
			print('Error querying \'{0}\''.format(collection))

	def count(self, collection, power_class = None):
		if power_class:
			power_class = lib.classify_power(power_class)
			count = self.db[collection].count({'class':power_class})
		else:
			count = self.db[collection].count()
		
		return count

	def create_collection_noid(self, collection):
		try:
			self.db.createCollection(collection, {autoIndexId: False})
		except:
			print('Error trying to create collection \'{0}\''.format(collection))

	def drop_collection(self, collection):
		try:
			self.db[collection].drop()
		except:
			print('Error trying to drop collection \'{0}\''.format(collection))

	def close_cursor(self):
		self.db.close()
