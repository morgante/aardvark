from flask import render_template
from flask import request

from Aardvark import Aardvark

import extract

import json

@Aardvark.route('/')
def index():
    return render_template('index.html')

@Aardvark.route('/analyze', methods=['POST'])
def analyze():
	url = request.form['file']

	html = extract.get_html(url)
	text = extract.html_to_text(html, fontfilter=True)

	acronyms = extract.get_acronyms(text)

	list = []

	for acronym in acronyms:
		list.append(acronym)

	return json.dumps(list)