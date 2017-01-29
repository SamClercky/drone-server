#!/usr/bin/env python

from Queue import Queue
from threading import Thread

q = Queue()

def loop1(q):
    while 1:
        q.put("Van t1")

def loop2(q):
    while 1:
        q.put("Van t2")

t1 = Thread(target=loop1, args=(q,))
t1.start()
t2 = Thread(target=loop2, args=(q,))
t2.start()

while 1:
    if not q.empty():
        print(q.get())
    else:
        print("leeg")
