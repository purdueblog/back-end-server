import time
from threading import Thread

class worker(Thread):
    def run(self):
        while(True):
            print("repeat")        
            time.sleep(10)


def one_time_startup():
    worker().start()