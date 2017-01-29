#!/usr/bin/env python

"""Startpunt voor het programme dat de drone"""

from pyMultiwii import MultiWii
from sys import stdout

class Main:
    """Startklasse van de applicatie"""

    def __init__(self):
        self.board = MultiWii("/dev/ttyACM0")
    
    def loop(self):
        try:
            while True:
                self.board.getData(MultiWii.ATTITUDE)
                #print board.attitude #uncomment for regular printing

                # Fancy printing (might not work on windows...)
                message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(self.board.attitude['angx']),float(self.board.attitude['angy']),float(self.board.attitude['heading']),float(self.board.attitude['elapsed']))
                stdout.write("\r%s" % message )
                stdout.flush()
                # End of fancy printing

        except Exception, err:
            print("ERROR: " + str(err))

if __name__ == "__main__":
    main = Main()
    main.loop()