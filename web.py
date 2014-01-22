from flask import Flask

import aardvark as vark
import json

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!"

@app.route("/test")
def test():
	p = 'examples/nyuad'

	text = vark.get_text(p)

	acronyms = vark.get_acronyms(text)
	table = {}

	for acronym in acronyms:
		table[acronym] = vark.expand(acronym, text)

	return json.dumps(table)

if __name__ == "__main__":
	app.run(debug=True)