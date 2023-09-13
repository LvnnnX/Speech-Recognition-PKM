import time
from threading import Thread

class programmer(Thread):
    def run(self):
        for x in range(0, 11):
            print(x)
            time.sleep(1)


class developer(Thread):
    def run(self):
        for x in range(200, 203):
            print(x)
            time.sleep(5)


print("Start thread")
programmer().start()
print("developer Thread")
developer().start()
print("Done")