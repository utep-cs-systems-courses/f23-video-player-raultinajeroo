from threading import *

class videoQueue:
    # Class for queuing / dequing video frames using mutex lock
    def __init__(self, frame_count = 32):
        self.storage = []
        self.storageLock = Lock()
        self.full = Semaphore(0)
        self.empty = Semaphore(frame_count)

    def enque(self, frame):
        self.empty.acquire()
        self.storageLock.acquire()
        self.storage.append(frame)
        self.storageLock.release()
        self.full.release()

    def deque(self):
        self.full.acquire()
        self.storageLock.acquire()
        frame = self.storage.pop()
        self.storageLock.release()
        self.empty.release()
        return frame