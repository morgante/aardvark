from flask import render_template
from flask import request

from Aardvark import Aardvark
import vark

import json

@Aardvark.route('/')
def index():
    return render_template('index.html')

@Aardvark.route('/analyze', methods=['POST'])
def analyze():
	url = request.form['file']

	# SPEED
	return open('Aardvark/cache/wef2.json').read()

	# For now, we just simulate for speed purposes
	p = 'examples/wef2'

	text = vark.get_text(p)

	acronyms = vark.get_acronyms(text)
	table = {}

	print acronyms

	for acronym in acronyms:
		table[acronym] = vark.expand(acronym, text)

	return json.dumps(table)