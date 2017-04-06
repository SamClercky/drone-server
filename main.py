#!/usr/bin/env python

"""Startpunt voor het programme van de drone"""

from classes.pyMultiwii import MultiWii
from sys import stdout
from classes.server import Server
from classes.gamepad import JoyStick
from multiprocessing import Queue
from threading import Lock


class Main:
    """Startklasse van de applicatie"""

    def __init__(self):
        self.queue = Queue()
        self.board = MultiWii("/dev/ttyACM0")
        self.board.getData(MultiWii.ATTITUDE)
        self.lock = Lock()
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
            else:
                self.excecute(previousMsg)

    def excecute(self, msg):
        """Executes the message"""
        data = self.formData(msg)
        self.board.sendCMD(8, MultiWii.SET_RAW_RC, data)

    def formData(self, msg):
        """Forms data-array"""
        data = str(msg).split("::")
        roll = 0
        pitch = 0
        yaw = 0
        throttle = 0

        if len(data) >= 2 and not data[1] == "":
            # prepare data
            data[1] = int(data[1])
            print(data[1])

            if data[0] == "HIGH":
                throttle = data[1]
            if data[0] == "LEFT":
                roll = -data[1]
            if data[0] == "RIGHT":
                roll = data[1]
            if data[0] == "FORWARD":
                pitch = data[1]
            if data[0] == "BACK":
                pitch = -data[1]
            if data[0] == "IDLE":
                pass
            if data[0] == "START":
                pass
            if data[0] == "STOP":
                roll = 0
                pitch = 0
                yaw = 0
                throttle = 0

            return [roll, pitch, yaw, throttle]

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
