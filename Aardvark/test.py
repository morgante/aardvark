import db
import extract
import vark_wiki as vark
from nltk import distance


examples = db.find('research')

total_tried = 0
total_successful = 0

for example in examples:

	url = example['pdf']

	print "testing: ", url

	all_text = extract.get_html(url)
	filtered_text = extract.html_to_text(all_text, fontfilter=True)

	print "... got text"

	acronyms = list(vark.get_acronyms(filtered_text))

	print "... got acronym"
	print acronyms

	tried = 0
	successful = 0

	for acronym, expansion in example['definitions'].iteritems():
		if len(expansion) >= 1:
			if (acronym not in acronyms):
				print "... Could not find %s (%s) in acronyms" % (acronym, expansion)
			else:
				tried += 1
				computed = vark.expand(acronym, all_text).strip().lower().replace('-',' ')
				expansion = expansion.strip().lower().replace('-',' ')
				ed = distance.edit_distance(computed, expansion)
				if ed < 3:
					print "... Success for %s: %s" % (acronym, computed)
					successful += 1
				else:
					print "... Incorrect expansion for %s: %s (expected %s)" % (acronym, computed, expansion)

	print '. Successful matches: %d / %d' % (successful, tried)

	total_tried += tried
	total_successful += successful

print 'Overall success rate: %d / %d' % (total_successful, total_tried)