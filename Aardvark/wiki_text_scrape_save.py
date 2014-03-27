''' This is for scraping the zipped wikipedia TXT files.
    1. Find acronym / definition pairs in each article
    2. Create articleid from url
    3. Save acronym/definition / articleid in one csv
    4. Save articleid/article in another

'''


import os
import sys
import time
import numpy as np
import re
import string
import csv
from vark import get_text
from vark_extract import get_font_filtered_text
from vark_wiki import definition_patterns, wiki_lookup, get_acronyms, text_expand
from nltk.stem import WordNetLemmatizer
from nltk import clean_html
from string import translate
from base64 import b64encode
# https://wikipedia.readthedocs.org/en/latest/


# write results to csv
folder_path = '/Users/Ben/Desktop/aardvark/Aardvark/'
defs_file_name = 'scraped_definitions.csv'
arts_file_name = 'scraped_articles.csv'

# Find files already seen:

csv.field_size_limit(sys.maxsize)

arts_file = open(folder_path+arts_file_name, 'r')
done_files=[]
reader = csv.reader(arts_file)
for line in reader:
    done_files.append(line[-1])

done_files = np.unique(done_files)
arts_file.close()

# Open files to append
defs_file = open(folder_path+defs_file_name, 'a')
arts_file = open(folder_path+arts_file_name, 'a')

max_files = 5000


#table = string.maketrans("","")
table = string.maketrans(string.punctuation+'\n', ' '*len(string.punctuation+'\n'))



art_writer = csv.writer(arts_file)
sd_writer = csv.writer(defs_file)

# Text Wikipedia
import gzip
import glob
import base64

wiki_path = folder_path + "wikipedia_txt_dump/"
total_files = len(os.walk(wiki_path).next()[2])


count=0
for zipname in glob.iglob(wiki_path+'*[0-9].txt.gz'):
    if zipname in done_files:
        print zipname
        continue
    count +=1
    if count > max_files:
        break
    print "\nFile number", count, "of", total_files
    scraped_arts, scraped_data = [], []
    f = gzip.open(zipname, 'r')
    articles = f.read().replace('\n', '')
    articles = [art.split("]]") for art in articles.strip().split("[[")]   # Subject, article pairs
    if len(articles[0])<2:
        articles.pop(0)
    articles = [[art[0], ' '.join(art[1:])] for art in articles]
    for title, article in articles[1:]:
        if title[:9]=='Wikipedia' or title[-16:]=='(disambiguation)' or title[:5]=='File:' or title[-4:]=='.css' or title[:8]=='Category' or title[:5].lower()=='media' or title[:5].lower()=='image' or title[:6].lower()==':image':

            continue
        print title
        articleid = base64.b64encode('https://en.wikipedia.org/wiki/'+title.replace(' ', '_'))
        acronyms = get_acronyms(article)
        def_count = 0
        for acronym in acronyms:
            patterns = definition_patterns(acronym)
            definition = text_expand(acronym, article, patterns)
            if definition:
                def_count +=1
                scraped_data.append([acronym, definition, articleid, title])
        if def_count > 0:
            scraped_arts.append([articleid, article, zipname])
    for line in scraped_arts:
        line[1] = unicode(line[1], errors ='ignore')
        line[1] = line[1][:30000].encode('ascii', 'ignore')
        line[1] = line[1].translate(table)
        art_writer.writerow(line)
    for line in scraped_data:
        sd_writer.writerow(line)


defs_file.close()
arts_file.close()


## After, ordering / filtering:
#defs_file = open(folder_path+defs_file_name, 'r')
#reader = csv.reader(defs_file)
#defs = []
#for line in reader:
#    defs.append(line)
#defs_file.close()
#
#arts_file = open(folder_path+arts_file_name, 'r')
#reader = csv.reader(arts_file)
#arts = []
#for line in reader:
#    arts.append(line)
#arts_file.close()
#
#
#defs = sorted(defs, key=lambda x:x[0])
#unique_acronyms = np.unique([d[0] for d in defs])
#
#acronym_counts = np.zeros(10)
#for acronym in unique_acronyms:
#    acronym_counts[len(acronym)]+=1
#
#print zip(range(10),acronym_counts)

