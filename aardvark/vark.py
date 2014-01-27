from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

import re
import os.path

from lxml.html import parse

import requests

import sys
import getopt


def write_text(path, text):
    file = open(path, "w")
    file.write(text)
    file.close()

def get_text(path):
    txt_path = path + '.txt'

    if (os.path.isfile(txt_path)):
        return open(txt_path).read()

    path = path + '.pdf'
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()

    write_text(txt_path, str)

    return str

def get_acronyms(text):
    pattern = r'\b(?:[A-Z]){2,}\b'

    acronyms = re.findall(pattern, text)

    return set(acronyms)

def get_cat_name(id):
    cats = {
        1: 'Most Common',
        2: 'Technology',
        4: 'Government & Military',
        8: 'Science & Medicine',
        64: 'Business',
        16: 'Organizations',
        32: 'Slang & jargon'
    }

    return cats[id]

def get_expansions(acronym):
    try:
        url = 'http://acronyms.thefreedictionary.com/' + acronym

        doc = parse(url).getroot()

        defs = []

        rows = doc.cssselect('table#AcrFinder tr:nth-child(n+1)')

        # Fill in out definitions
        for i, row in enumerate(rows):
            category = row.get('cat')
            cells = row.cssselect('td')

            if (len(cells) >= 2):
                meaning = cells[1].text_content()
                score = float(float(len(rows) - i) / float(len(rows)))
                defs.append([meaning, category, score])

        return defs;
    except:
        return []

def expand(acronym, text):
    pattern = r'('

    for i, s in enumerate(acronym):
        pattern += '' + s + '[A-Za-z]+'
        if (i < len(acronym) - 1):
            pattern += ' '
    pattern += ')'

    matches = re.findall(pattern, text)
    expansions = dict.fromkeys(matches, 10)

    for expansion in get_expansions(acronym):
        score = int(expansion[2] * 10)

        if expansion[0] in expansions:
            expansions[expansion[0]] += score
        else:
            expansions[expansion[0]] = score


    return expansions

# args = getopt.getopt(sys.argv[1:], "ho:v")
# p = os.path.splitext(args[1][0])[0]

# text = get_text(p)

# acronyms = get_acronyms(text)
# table = {}

# for acronym in get_acronyms(text):
#     table[acronym] = expand(acronym, text)

# for key, value in table.iteritems():
#     print key, value.keys()