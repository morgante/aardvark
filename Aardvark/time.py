import time

import db
import extract
import vark_wiki as vark
from nltk import distance

example = 'https://www.filepicker.io/api/file/tVG2ge5QQSm12RJGC8sF'

t0 = time.clock()

print 'Starting at %d' % t0

all_text = extract.get_text(example)

t1 = time.clock()

print 'Got text at %d' % t1

print all_text

print 'Total time'
print (t1 - t0)