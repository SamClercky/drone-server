#!/usr/bin/env python

"""Dit is de server klasse van de applicatie"""

from tornado import web, ioloop, queues, websocket
import os
from classes.pyMultiwii import MultiWii
from threading import Thread

global q      # A global queue var
global board  # A global MultiWii var
global lock   # A global lock

class Server():
    """Server klasse"""

    def __init__(self, myBoard, qu, myLock, poort=8888):
        global board
        global q
        global lock
        board = myBoard
        q = qu
        print(q)
        lock = myLock

        self.poort = poort
        self.app   = web.Application([
            (r"/", MainHandler),
            (r"/webs", MySocket)
        ])
        self.app.listen(8888)
    
    def start(self):
        self.tornado = Thread(target=ioloop.IOLoop.current().start)
        self.tornado.start()
    
    def stop(self):
        ioloop.IOLoop.current().stop()

class MainHandler(web.RequestHandler):

    def get(self):
        self.write(open("www/index.html", "r").read())

class MySocket(websocket.WebSocketHandler):

    inProssess = False
        
    def check_origin(self, origin):
        return True

    def open(self):
        print("Websocket opened")
    
    def on_message(self, msg):
        msg = str(msg).split("//")
        if msg[0] == "get":
            self.write_message(self.getData())
        elif msg[0] == "set":
            self.sendData(msg[1])
        

    def getData(self):
        result = None
        if not self.inProssess:
            self.inProssess = True
            try:
                result = self.getMsgFromM()
            except Exception, error:
                print(error)
                result = "False"
            self.inProssess = False
        else:
            result = "False"
        return result

    def sendData(self, msg):
        global q
        #print(msg)
        q.put(msg)
    
    def on_close(self):
        print("Socket closed")
    
    def getMsgFromM(self):
        global board
        global lock
        result = None
        try:
            lock.acquire()
            board.getData(MultiWii.ATTITUDE)
            result = board.attitude
            lock.release()
        except Exception, error:
            result = str(error)
        return result
