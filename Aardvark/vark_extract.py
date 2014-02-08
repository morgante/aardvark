
import os, sys
import time
import vark

from pdfminer.converter import HTMLConverter
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



def get_html(path): # Pulls html from PDF instead of plain text
    if path[-4:]!=".pdf":
        path=path+".pdf"
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
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
    return str

def html_to_text(htmltext, fontfilter=True):
    def repl_fs(m): # Munging to create font size tags
        size = m.group(3)
        return "[fontsize__"+size+"]"
    txt = re.sub(r"<(.*)(font-size:)(\d+).*>",repl_fs, htmltext)
    txt = re.sub('<.*>','',txt)
    if fontfilter:
        fontcounts={}
        fs = 0
        for w in txt.split():   # Count font sizes
            if w[:11]=="[fontsize__":
                fs = re.search("\d+", w).group(0)
            else:
                if fs not in fontcounts:
                    fontcounts[fs]=0
                fontcounts[fs]+=1
        main_font = int(max(fontcounts, key=fontcounts.get))
        filtered_text=[]
        for w in txt.split():
            if w[:11]=="[fontsize__":
                fs = int(re.search("\d+", w).group(0))
            elif np.abs(fs-main_font)<2:    # Keep 2 font sizes near main font
                filtered_text.append(w)
        txt = ' '.join(filtered_text)
        vark.write_text(path+".txt", txt)
    return txt

def get_font_filtered_text(path):   # Takes path, returns text
    txt_path = path + '.txt'
    if (os.path.isfile(txt_path)):
        return open(txt_path).read()
    htmltext = get_html(path)   # This needs to be optimized eventually
    return html_to_text(htmltext, fontfilter=True)

#
#path = 'examples/fwc'
## Example with font filtering
#t0 = time.time()
#text = get_font_filtered_text(path)
#print "Time:", time.time() - t0
#
## Example without font filtering
#t0 = time.time()
#text = vark.get_text(path)
#print "Time:", time.time() - t0
