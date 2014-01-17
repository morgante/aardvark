from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

import re
import os.path

from bs4 import BeautifulSoup
from lxml.html import parse

import requests


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

    return acronyms

def get_expansions(acronym):
    url = 'http://www.acronymfinder.com/~/search/af.aspx?string=exact&Acronym=' + acronym

    # r  = requests.get(url)
    # data = r.text

    # soup = BeautifulSoup(data)
    doc = parse(url).getroot()

    cells = doc.cssselect('table#ListResults tr:nth-child(n+3) td:nth-child(3)')

    defs = {}

    for cell in cells:
        defs.append(cell.text_content())

    return defs;

def expand(acronym, text):
    pattern = r'('

    for i, s in enumerate(acronym):
        pattern += '' + s + '[A-Za-z]+'
        if (i < len(acronym) - 1):
            pattern += ' '
    pattern += ')'

    matches = re.findall(pattern, text)
    expansions = dict.fromkeys(matches, 1)

    return expansions

p = 'examples/lte'

text = get_text(p)

acronyms = get_acronyms(text)
table = {}

print get_expansions(acronyms[0])

for acronym in get_acronyms(text):
    table[acronym] = expand(acronym, text)

print table