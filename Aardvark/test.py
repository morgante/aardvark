import db
import extract

import vark_wiki as vark


examples = db.find('research')

for example in examples:

	url = example['pdf']

	print "testing: ", url

	html = extract.get_html(url)
	text = extract.html_to_text(html, fontfilter=True)

	print "... got text"

	acronyms = list(vark.get_acronyms(text))[:10]

	print "... got acronysm"
	print acronyms

	for acronym in acronyms:
		expansion = vark.expand(acronym, text)

		print (acronym, expansion)