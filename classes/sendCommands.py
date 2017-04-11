#!/usr/bin/env python

from threading import Lock, Thread
from classes.pyMultiwii import MultiWii

class SendCommands:
    board = None
    cmd = [1500, 1500, 2000, 1000, 1000, 1040, 1000, 1000] # init setup
    thread = None

    def __init__(self, board):
        self.board = board
        self.start()

    def start(self):
        print("sendCommands loop starts")
        self.thread = Thread(target=self._loop)
        self.thread.setDaemon(True)
        self.thread.start()

    def _loop(self):
        while True:
            cmd = self.cmd
            print("loop: " + str(cmd))
            self.board.sendCMD(16, MultiWii.SET_RAW_RC, cmd)

            print(self.board.attitude)

    def _formData(self, msg, prevData):
        """Forms data-array"""
        data = str(msg).split("::")
        roll = prevData[0]
        pitch = prevData[1]
        yaw = prevData[2]
        throttle = prevData[3]
        aux1 = prevData[4]
        aux2 = prevData[5]
        aux3 = prevData[6]
        aux4 = prevData[7]

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
                roll = 1500
                pitch = 1500
                yaw = 2000
                throttle = 1000
            if data[0] == "STOP":
                roll = 1500
                pitch = 1500
                yaw = 1000
                throttle = 1000


        return [roll, pitch, yaw, throttle, aux1, aux2, aux3, aux4]

    def excecute(self, msg):
        """brings msg into queue"""
        print(msg)
        self.cmd = self._formData(msg, self.cmd)
