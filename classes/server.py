#!/usr/bin/env python

"""Dit is de server klasse van de applicatie"""

from tornado import web, ioloop, queues

global q

class Server():
    """Server klasse"""

    def __init__(self, qu, poort=8888):
        self.poort = poort
        self.app   = tornado.web.Application([
            (r"/", MainHandler)
        ])
        self.app.listen(8888)
        q = qu
    
    def start(self):
        ioloop.IOLoop.current().start()
    
    def stop(self):
        ioloop.IOLoop.current().stop()

class MainHandler(web.RequestHandler):

    def get(self):
        self.write("Hallo, installeer deze app om alles te kunnen zien")

