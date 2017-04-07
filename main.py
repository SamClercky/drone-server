#!/usr/bin/env python

"""Startpunt voor het programme van de drone"""

from classes.pyMultiwii import MultiWii
from sys import stdout
from classes.server import Server
from classes.gamepad import JoyStick
from classes.sendCommands import SendCommands
from multiprocessing import Queue
from threading import Lock


class Main:
    """Startklasse van de applicatie"""

    def __init__(self):
        self.queue = Queue()
        self.board = MultiWii("/dev/ttyACM0")
        self.board.getData(MultiWii.ATTITUDE)
        self.lock = Lock()
        self.sendCommands = SendCommands(self.board)
        print("Eerste data ontvangen")
        # Starten met starten van server en joystick
        self.server = Server(self.board, self.queue, self.lock, 8888)
        print("server aangeroepen")
        self.server.start()
        print("Server gestart")
        self.joystick = JoyStick(self.queue)
        self.joystick.start()
        print("JoyStick is begonnen")

    def loop(self):
        """Starts the main loop"""
        previousMsg = ""
        while 1:
            if not self.queue.empty():
                msg = self.queue.get()
                self.excecute(msg)
                previousMsg = msg

    def excecute(self, msg):
        """Executes the message"""
        self.sendCommands.excecute(msg)

if __name__ == "__main__":
    try:
        main = Main()
        print("Main aangeroepen")
        main.loop()
    except KeyboardInterrupt:
        main.server.stop()
        main.joystick.stop()
        for t in enumerate():
            if t.isAlive():
                t._Thread_stop()
        exit(0)
