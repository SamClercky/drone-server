#!/usr/bin/python
"""Alles wat te maken heeft met gamepads"""

from evdev import InputDevice, categorize, ecodes, KeyEvent
from multiprocessing import Queue
from threading import Lock
from threading import Thread

class JoyStick:
    """A controller class who monitors the user input via a logitech f710 gamepad"""

    def __init__(self, q):
        self.q = q
        self.gamePad = InputDevice('/dev/input/event0')
        self.started = False
        self.lock = Lock()
        self.thread = None

    def __loop(self, q, lock):
        """Should run in separate thread"""
        lock.acquire()
        run = self.started
        gamePad = self.gamePad
        lock.release()

        for e in gamePad.read_loop():
            # Kijken wat er gebeurt en dit doorgeven aan de rest v/h programma
            x = e.code
            v = e.value
            if x == 315:
                q.put("START::" + str(v))
            elif x == 314:
                q.put("STOP::" + str(v))
            elif x == 16:
                q.put("LEFT::" + str(self.__nomelize(v, 1, 65535)))
            elif x == 16:
                q.put("RIGHT::" + str(self.__nomelize(v, 1, 65535)))
            elif x == 17:
                q.put("FORWARD::" + str(self.__nomelize(v, 1, 65535)))
            elif x == 17:
                q.put("BACK::" + str(self.__nomelize(v, 1, 65535)))
            elif x == 5:
                q.put("HIGH::" + str(self.__nomelize(v, 255, 65535)))
            elif x != 0:
                q.put("IDLE::")

            # checken of alles nog oke is en updaten v/d data
            if run == False:
                # Als de loop moet stoppen stopt hij
                break
            lock.acquire()
            run = self.started
            lock.release()

    def start(self):
        """Starts the thread"""
        self.started = True
        self.thread = Thread(target=self.__loop, args=(self.q, self.lock))
        self.thread.start()

    def stop(self):
        """Stops the thread"""
        if self.thread != None:
            self.started = False
            if self.thread.is_alive():
                self.thread.join()

    def __nomelize(self, num, max1 = 255, max2 = 10000):
        """Normelizes all the numbers to a number that is readable for other things"""
        result = int(float(num) * max2 / max1)
        if num == 1:
            result = max2
        return int(float(num) * max2 / max1)