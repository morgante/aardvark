#!/usr/bin/env python
from pymongo import MongoClient
import os

if ('DB_PORT_27017_TCP_ADDR' in os.environ):
	host = os.environ['DB_PORT_27017_TCP_ADDR']
else:
	host = 'tugboat.nyuad.org'

if ('DB_PORT_27017_TCP_PORT' in os.environ):
	port = int(os.environ['DB_PORT_27017_TCP_PORT'])
else:
	port = 49220

if ('ENV' in os.environ and os.environ['ENV'] == 'prod'):
	db_name = 'production'
elif ('ENV' in os.environ and os.environ['ENV'] == 'test'):
	db_name = 'test'
else:
	db_name = 'development'

client = MongoClient(host, port)
db = client[db_name]

def insert(collection, data):
	db[collection].insert(data)

def find_one(collection, query={}, fields=None):
	return db[collection].find_one(query, fields=fields)

def find(collection, query={}, fields=None):
	return db[collection].find(query, fields=fields)

# Usage:
# 
# define("NYU")
# 
# Returns a list of ex. [{definition: "New York University", "article": "American Higher Education", "text": "In America today, ..."}]
def define(acronym):
	docs = find("definitions", {"acronym": acronym})

	defs = []

	for doc in docs:
		article = find_one("articles", {"aid": doc["aid"]})
		
		defs.append({
			"definition": doc["definition"],
			"article": doc["article"],
			"text": article["text"]
		})

	return defs