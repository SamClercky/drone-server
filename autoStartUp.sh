#!/usr/bin/env bash

# shout run inside rc.local

(
    python /home/pi/Documents/drone/main.py
    echo $?
 ) & > /home/pi/droneLog.txt