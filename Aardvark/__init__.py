import os
import tornado.escape
import tornado.ioloop
import tornado.web
from tornado.web import asynchronous
from multiprocessing.pool import ThreadPool

import extract
import db
import vark_wiki as vark
import json

import logging

logging.basicConfig(level=logging.DEBUG)

_workers = ThreadPool(10)
 
def run_background(func, callback, args=(), kwds={}):
    def _callback(result):
        tornado.ioloop.IOLoop.instance().add_callback(lambda: callback(result))
    _workers.apply_async(func, args, kwds, _callback)
 
# blocking task like querying to MySQL
def blocking_task(url):
	text = extract.get_text(url)

	acronyms = vark.get_acronyms(text)

	items = []

	print acronyms

	for acronym in acronyms:
		print acronym
		expansion = vark.expand(acronym, text)
		print expansion
		items.append({
			"acronym": acronym,
			"definition": expansion
			})

	return items
 
class Analyzer(tornado.web.RequestHandler):
    @asynchronous
    def post(self):
    	url = self.get_argument('file')

        run_background(blocking_task, self.on_complete, (url,))
 
    def on_complete(self, res):
        self.write(json.dumps(res))
        self.finish()

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

handlers = [
	(r"/", MainHandler),
	(r"/analyze", Analyzer)
]

settings = dict(
	template_path=os.path.join(os.path.dirname(__file__), "templates"),
	static_path=os.path.join(os.path.dirname(__file__), "static")
)

application = tornado.web.Application(handlers, **settings)

def run():
	application.listen(5000)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	run()