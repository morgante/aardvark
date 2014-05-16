from flask import render_template
from flask import request

from Aardvark import Aardvark

import extract
import db
import vark_wiki as vark

import json

@Aardvark.route('/')
def index():
    return render_template('index.html')

@Aardvark.route('/analyze', methods=['POST'])
def analyze():
	url = request.form['file']

	text = extract.get_text(url)

	acronyms = vark.get_acronyms(text)

	list = []

	print acronyms

	for acronym in acronyms:
		expansion = vark.expand(acronym, text)
		print expansion
		list.append({
			"acronym": acronym,
			"definition": expansion
			})

	return json.dumps(list)

@Aardvark.route('/identity', methods=['POST'])
def identify():
	url = request.form['file']

	text = extract.get_text(url)

	acronyms = extract.get_acronyms(text)

	list = []

	for acronym in acronyms:
		list.append(acronym)

	return json.dumps(list)

@Aardvark.route('/submit', methods=['POST'])
def submit():

	form = request.form

	data = {
		"definitions": {}
	}

	for field in form:
		if (field == 'pdf'):
			data["pdf"] = form[field]
		else:
			data['definitions'][field] = form[field]

	db.insert('research', data)

	return render_template('thanks.html')