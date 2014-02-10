
import os
#os.chdir("Desktop/aardvark/Aardvark")

from vark import get_text
from vark_extract import get_font_filtered_text

import time
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import pairwise_distances
from nltk import word_tokenize, regexp_tokenize, clean_html
from nltk.stem import WordNetLemmatizer
import wikipedia


def get_acronyms(text): # Find Acronyms in text
    pattern = r'\b[A-Z]{2,}s{0,1}\b'
    acronyms = re.findall(pattern, text)
    return set(acronyms)


def definition_patterns(acronym):   # Create definition regex patterns from acronym
    def_pattern=r''
    between_chars = r'\w+[.-]{0,1}\s{0,1}(?:\w{2,5}[.-]{0,1}\s{0,1}){0,1}'
    for i,c in enumerate(acronym):
        c = "["+c+c.lower()+"]"
        if i==0:
            def_pattern += r'\b'+c+between_chars
        elif i<len(acronym)-1:
            def_pattern += c+between_chars   # acronym letter, chars, periods, space
        else:
            def_pattern += c+r'\w+\b'
    patterns = [def_pattern+r'(?=\W*(?:or\s){0,1}'+acronym+r')',r'(?<='+acronym+r'\s\W)'+def_pattern, def_pattern+r'(?=\W*(?:or\s){0,1}'+acronym+r's)',r'(?<='+acronym+r's\s\W)'+def_pattern]   # Doubled patters for plural acronyms... OPTIMIZE later
    patterns = [re.compile(pattern) for pattern in patterns]
    return patterns



def text_expand(acronym, text, patterns):   # Search original text for acronyms
    patterns = definition_patterns(acronym)
    for pattern in patterns:
        pattern_result = re.findall(pattern, text)
        if pattern_result:
            return pattern_result[0]
    return None


def wiki_lookup(acronym, patterns): # Lookup acronym on wikipedia
    patterns = definition_patterns(acronym)
    definitions = []
    for result in wikipedia.search(acronym):
        if result[-16:]=='(disambiguation)':
            pass
        try:
            page = wikipedia.page(result)
            content = page.content
            for pattern in patterns:
                pattern_result = re.findall(pattern, content)
                if pattern_result:
                    definitions.append([pattern_result[0], content])
                    break
        except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError, TypeError):
            pass
    return np.array(definitions)


class CleanLemmaTokenizer(object):  # HTML stripper and stemmer
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in regexp_tokenize(clean_html(doc), '\w\w+')]

def wiki_expand(acronym, text, patterns):   # Chooses expansion from wiki
    t0 = time.time()
    results = wiki_lookup(acronym, patterns)
    if len(results)==0:
        definition="NONE FOUND"
    else:
        definitions, articles = results[:,0], results[:,1]
        myTokenizer=CleanLemmaTokenizer()
        vectorizer = TfidfVectorizer(max_df=1.0, max_features=10000, tokenizer=myTokenizer,stop_words='english', use_idf=True, binary=False, decode_error='ignore')
        X = vectorizer.fit_transform(articles)
        s = vectorizer.transform([text])
        D = pairwise_distances(X, s)
        definition = definitions[argmin(D)]
    return definition

def expand(acronym,text):   # Top level expansion function, calls others
    try:
        patterns = definition_patterns(acronym)
        definition = text_expand(acronym, text, patterns)
        if definition:
            return definition+" (from text)"
        else:
            return wiki_expand(acronym, text, patterns)+" (from wikipedia)"
    except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError, TypeError):



## Example pipeline
#t00 = time.time()
#path = '/Users/Ben/Desktop/aardvark/examples/fwc'
#print "Path:", path
#print "Extracting Text..."
#t0 = time.time()
#filtered_text = get_font_filtered_text(path)
#all_text = get_text(path)
#print "Time:", time.time() - t0
#print "Extracting Acronyms..."
#t0 = time.time()
#acronyms = list(get_acronyms(filtered_text))[:10]# Limit to 10 (for now, for time)
#print "Time:", time.time() - t0
#print "Scrubbing and Selecting Definitions..."
##result = [(acronym, expand(acronym,text)) for acronym in acronyms]
#print "\n******    RESULTS    ******"
##for acronym, expansion in result:
##    print acronym+':', expansion
#result = []
#text_count = 0
#wiki_count = 0
#for acronym in acronyms:
#    definition = ' '.join(expand(acronym,all_text).split())
#    result.append([acronym, definition])
#    print acronym+':', definition
#    if definition[-5:]=="text)":
#        text_count+=1
#    else:
#        wiki_count+=1
#print "\nFrom Text:", text_count
#print "\nFrom Wiki:", wiki_count
#print "\nTotal Time:", time.time()-t00



