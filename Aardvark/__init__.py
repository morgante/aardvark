import os
import tornado.escape
import tornado.ioloop
import tornado.web

import extract
import db
import vark_wiki as vark
import json

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

class AnalyzeHandler(tornado.web.RequestHandler):
	def post(self):
		url = self.get_argument('file')

		text = extract.get_text(url)

		acronyms = vark.get_acronyms(text)

		list = []

		print acronyms

		for acronym in acronyms:
			expansion = vark.expand(acronym, text)
			print expansion
			list.append({
				"acronym": acronym,
				"definition": expansion
				})

		self.write(json.dumps(list))

handlers = [
	(r"/", MainHandler),
	(r"/analyze", AnalyzeHandler)
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