import vark

p = 'examples/wef2'

text = vark.get_text(p)

acronyms = vark.get_acronyms(text)
table = {}

print acronyms

for acronym in acronyms:
	table[acronym] = vark.expand(acronym, text)

print json.dumps(table)