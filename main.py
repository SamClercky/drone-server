#!/usr/bin/env python

"""Startpunt voor het programme van de drone"""

from classes.pyMultiwii import MultiWii
from sys import exit
from classes.server import Server
from classes.gamepad import JoyStick
from classes.sendCommands import SendCommands
from multiprocessing import Queue
from threading import Lock
import subprocess
from time import sleep
import datetime


class Main:
    """Startklasse van de applicatie"""

    def __init__(self):
        self.queue = Queue()
        self.board = MultiWii("/dev/ttyACM0")
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
        if msg == "STOPSTOP::":
            raise Exception
        self.sendCommands.excecute(msg)

if __name__ == "__main__":
    print("Starting at " + datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S'))
    try:
        print("Sleeping till system is fully opperationel...")
        sleep(8)
        main = Main()
        print("Main aangeroepen")
        main.loop()
    except KeyboardInterrupt:
        main.server.tornado.join(0.0)
        main.joystick.thread.join(0.0)
        main.sendCommands.thread.join(0.0)
        exit(0)
    except Exception:
        subprocess.Popen(["sudo", "shutdown", "-h", "now"])
        main.server.tornado.join(0.0)
        main.joystick.thread.join(0.0)
        main.sendCommands.thread.join(0.0)
        exit(1)
