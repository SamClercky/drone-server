#!/usr/bin/env python

from threading import Lock, Thread
from classes.pyMultiwii import MultiWii

class SendCommands:
    board = None
    cmd = [1500, 1500, 2000, 1000] # init setup
    lock = Lock()
    thread = None

    def __init__(self, board):
        self.board = board
        self.start()

    def start(self):
        print("sendCommands loop starts")
        self.thread = Thread(target=self._loop)
        self.thread.start()

    def _loop(self):
        while True:
            print("loop")
            self.lock.acquire()
            cmd = self.cmd
            self.lock.release()
            self.board.sendCMD(8, MultiWii.SET_RAW_RC, cmd)

    def _formData(self, msg, prevData):
        """Forms data-array"""
        data = str(msg).split("::")
        roll = prevData[0]
        pitch = prevData[1]
        yaw = prevData[2]
        throttle = prevData[3]

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


        return [roll, pitch, yaw, throttle]

    def excecute(self, msg):
        """brings msg into queue"""
        print(msg)
        self.lock.acquire()
        data = [msg, self.cmd]
        self.lock.release()
        data = self._formData(data[0], data[1])
        self.lock.acquire()
        self.cmd = data
        self.lock.release()