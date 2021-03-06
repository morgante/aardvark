
import os
#os.chdir("Desktop/aardvark/Aardvark")
import db as db
from vark_extract import get_font_filtered_text, get_text
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.svm import LinearSVC
from nltk import word_tokenize, regexp_tokenize, clean_html
from nltk.stem import WordNetLemmatizer
import string
from sklearn.externals import joblib

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
vectorizer = joblib.load(os.path.join(script_dir, "vectorizer"))

def get_acronyms(text): # Find Acronyms in text
    english_words = set(word.strip().lower() for word in open(os.path.join(script_dir, "wordsEn.txt")))
    pattern = r'\b[A-Z]{3,8}s{0,1}\b'   # Limit length 8
    acronyms = re.findall(pattern, text)
    acronyms = [acronym for acronym in acronyms if acronym.lower() not in english_words]
    return set(acronyms)


def definition_patterns(acronym):   # Create definition regex patterns from acronym
    def_pattern1,def_pattern2 = r'',r''
    between_chars1 = r'\w{3,}[-\s](?:\w{2,5}[-\s]){0,1}'
    between_chars2 = r'\w+[-\s]{0,1}(?:\w{2,5}[-\s]{0,1}){0,1}'
    for i,c in enumerate(acronym):
        c = "["+c+c.lower()+"]"
        if i==0:
            def_pattern1 += r'\b'+c+between_chars1
            def_pattern2 += r'\b'+c+between_chars2
        elif i<len(acronym)-1:
            def_pattern1 += c+between_chars1   # acronym letter, chars, periods, space
            def_pattern2 += c+between_chars2
        else:
            def_pattern1 += c+r'\w+\b'
            def_pattern2 += c+r'\w+\b'
    acronym = r''+acronym+r'\b'
    patterns=[]
    for def_pattern in [def_pattern1, def_pattern2]:
        patterns=patterns+[def_pattern+r'(?=\sor\s{0,1}(?:the\s){0,1}(?:a\s){0,1}'+acronym+r')',
                           def_pattern+r'(?=["(\s,]{2,}(?:or\s){0,1}(?:the\s){0,1}["]{0,1}'+acronym+r')',
                           r'(?<='+acronym+r'\s\W)'+def_pattern]
    patterns = [re.compile(pattern) for pattern in patterns]
    return patterns



def text_expand(acronym, text, patterns):   # Search original text for acronyms
    for pattern in patterns:
        pattern_result = re.findall(pattern, text)
        if pattern_result:
            return pattern_result[0]
    return None

def db_lookup(acronym): # Lookup acronym in database
    definitions = []
    results = list(db.define(acronym))
    if acronym[-1]=='s':    # If acronym is plural form, search singular also
        results += list(db.define(acronym[:-1]))
    for result in results:
        if result['article'][-16:]=='(disambiguation)':
            pass
        text = result['text']
        definition=result['definition']
        definitions.append([definition,text])
    return np.array(definitions)

#def distinct_results(results):  # This relies on db returning ordered results
#    count = len(results)
#    if count <= 1:
#        return False
#    else:
#        res1 = results[0][0].strip().lower().replace('-',' ')
#        res1 = ' '.join([w[:4] for w in res1.split()])
#        res2 = results[-1][0].strip().lower().replace('-',' ')
#        res2 = ' '.join([w[:4] for w in res2.split()])
#        if res1 != res2:
#            return True
#        return False

def db_expand(acronym, text):   # Chooses expansion from db
    results = db_lookup(acronym)
    if len(results)==0:
        pred_exp ="NONE FOUND"
#    elif not distinct_results(results):    # This WOULD be way faster if db returned ordered results
#        pred_exp = results[0][0]
    elif len(np.unique(results[:,0]))<2:
        pred_exp = results[0][0]
    else:
        definitions, articles = results[:,0], results[:,1]
        X = vectorizer.transform(articles)
        clf = LinearSVC(C=1., loss='l1')
        Y = definitions
        clf.fit(X,Y)
        s = vectorizer.transform([text.translate(string.maketrans("",""), string.punctuation)])
        pred_exp = clf.predict(s)[0]
    return pred_exp

def expand(acronym,text):   # Top level expansion function, calls others
    patterns = definition_patterns(acronym)
    definition = text_expand(acronym, text, patterns)
    if definition:
        return definition+" (from text)"
    else:
        return db_expand(acronym, text)

def same_exp(true_exp, pred_exp):
    true_exp = true_exp.strip().lower().replace('-',' ')
    pred_exp=' '.join([w[:4] for w in pred_exp.split()])
    true_exp=' '.join([w[:4] for w in true_exp.split()])
    if pred_exp == true_exp:
        return True
    #    ed = distance.edit_distance(pred_exp, true_exp)
    #    if ed < 3:
    #        return True
    return False

'''
Preprocessing:

For definitions:
expantion.strip().lower().replace('-',' ')

For articles:
Instead of live, all text should be changed to:
text.translate(string.maketrans("",""), string.punctuation)

possibly tokenized
try a shared vectorizer
'''

#
## To create shared vectorizer
## We need to save this and make it accessible from the app
#vect_articles = []
#while len(vect_articles)<10000:
#    k=random.choice(acronymdb.values())[0][1]
#    vect_articles.append(articledb[k])
#
#vectorizer = TfidfVectorizer(max_df=1.0, max_features=10000, stop_words='english', use_idf=True, binary=False, decode_error='ignore')
#vectorizer.fit(vect_articles)
#
## To save
#joblib.dump(vectorizer,"vectorizer")
#

## To load
#vectorizer = joblib.load("vectorizer")


## Example pipeline
#import time
#t00 = time.time()
#path = '/Users/Ben/Desktop/aardvark/examples/peerPaper'
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
#    acr_t0 = time.time()
#    print acronym
#    definition = ' '.join(expand(acronym,all_text).split())
#    result.append([acronym, definition])
#    print acronym+':', definition, time.time() - acr_t0
#    
##    result1 = len(db_lookup(acronym))
##    if result1 > 0:
##        if acronym in acronymdb:
##            result2 = len(acronymdb[acronym])
##            if acronym[-1]=='s' and acronym[:-1] in acronymdb:# plural / sing forms
##                result2 += len(acronymdb[acronym[:-1]])
##            print result1, result2
#
#    if definition[-5:]=="text)":
#        text_count+=1
#    else:
#        wiki_count+=1
#
#print "\nFrom Text:", text_count
#print "\nFrom Wiki:", wiki_count
#print "\nTotal Time:", time.time()-t00



