import csv

import Aardvark.db as db

articles = csv.reader(open('data/scraped_articles.csv', 'rb'), delimiter=',')
definitions = csv.reader(open('data/scraped_definitions.csv', 'rb'), delimiter=',')

n = 0

print 'starting to import articles'

for row in articles:
	id = row[0]
	text = row[1]
	source = row[2]

	db.insert('articles', {
		"aid": id,
		"text": text,
		"source": 'wikipedia'
	})

	n += 1

	print "stored %d articles" % n

print 'starting to import definitions'

n = 0

for row in definitions:
	acronym = row[0]
	definition = row[1]
	aid = row[2]
	article = row[3]

	db.insert('definitions', {
		"acronym": acronym,
		"definition": definition,
		"aid": aid,
		"article": article
	})

	n += 1

	print "stored %d definitions" % n

print 'finished importing'