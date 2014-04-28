import os, sys
import time

import urllib2

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

from urllib2 import Request
from StringIO import StringIO

import subprocess
import tempfile

import numpy as np

def get_text(url):
    pdf = urllib2.urlopen(Request(url)).read()

    tf = tempfile.NamedTemporaryFile()
    tf.write(pdf)
    tf.seek(0)

    outputTf = tempfile.NamedTemporaryFile()

    if (len(pdf) > 0) :
        out, err = subprocess.Popen(["pdftotext", "-layout", tf.name, outputTf.name ]).communicate()
        return outputTf.read()
    else :
        return None

def get_acronyms(text): # Find Acronyms in text
    pattern = r'\b[A-Z]{2,}s{0,1}\b'
    acronyms = re.findall(pattern, text)
    return set(acronyms)