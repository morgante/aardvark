import db
import extract

import vark_wiki as vark

examples = db.find('research')

total_tried = 0
total_successful = 0

for example in examples:

	url = example['pdf']

	print "testing: ", url

	html = extract.get_html(url)
	text = extract.html_to_text(html, fontfilter=True)

	print "... got text"

	acronyms = list(vark.get_acronyms(text))[:10]

	print "... got acronysm"
	print acronyms

	tried = 0
	successful = 0

	for acronym, expansion in example['definitions'].iteritems():
		if len(expansion) >= 1:
			tried += 1
			if (acronym not in acronyms):
				print "... Could not find %s in acronyms" % acronym
			else:
				computed = vark.expand(acronym, text)
				if computed.lower() == expansion.lower():
					'... Success for %s: %s' % (acronym, computed)
					successful += 1
				else:
					print "... Incorrect expansion for %s: %s (expected %s)" % (acronym, computed, expansion)

	print '. Successful matches: %d / %d' % (successful, tried)

	total_tried += tried
	total_successful += successful

print 'Overall success rate: %d / %d' % (total_successful, total_tried)