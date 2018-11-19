import threading
from threading import Lock
from threading import Semaphore

class Q:
    def __init__(self, bufCap, initArray = []):
        self.a = []
        self.a = [x for x in initArray]
        self.putSemaphore = threading.Semaphore(bufCap)
        self.getSemaphore = threading.Semaphore(0) #Adding the semaphores.

    def put(self, item):
        self.putSemaphore.acquire() #Remove 1 from available spots in queue.
        self.a.append(item)
        self.getSemaphore.release() #Add 1 to available removals from queue.

    def get(self):
        self.getSemaphore.acquire() #Same logic as before.
        a = self.a
        item = a[0]
        del a[0]
        self.putSemaphore.release()
        return item

    def __repr__(self):
        return "Q(%s)" % self.a