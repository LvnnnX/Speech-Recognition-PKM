# Membaca input dari robot bagian bawah (Arduino via Serial)
import serial
import threading

from lib.BrainDead_Models.models.generated.transform_pb2 import Transform
from src.state import CurrentState
from src.gut.abstract import AbstractGut
from src.models.transform_force import TransformForce
from src.gut.gut_helpers import parseGutString
import config as CONFIG


class SerialClient(AbstractGut):
    def __init__(self, comport=CONFIG.GUT_SERIAL_PORT, baud_rate=9600):
        self.com_port = comport
        self.is_running = False
        self.baud_rate = baud_rate
        self.currentState = CurrentState.getInstance()

    def loop(self):
        # Read and record the data
        data = []                       # empty list to store the data
        while self.is_running:
            try:
                b = self.channel.readline()         # read a byte string
                string_n = b.decode()  # decode byte string into Unicode
                string = string_n.rstrip()  # remove \n and \r
                # flt = float(string)        # convert string to float
                parsed = parseGutString(string)
                self.currentState.updateGutToBrain(parsed)
                # print(parsed)

                transform = Transform()
                transform.encXcm = parsed.absX
                transform.encYcm = parsed.absY
                transform.encROT = parsed.gyro
                self.currentState.updateMyTransform(transform)
                # print(transform)

                # data.append(flt)           # add to the end of data list
                # time.sleep(0.1)            # wait (sleep) 0.1 seconds
            except Exception as e:
                print("Gagal membaca gut line buffer: ", e)
                continue

    def send(self, msg):
        if self.channel.is_open:
            self.channel.write(msg)
        else:
            print("Attempted to send data via closed serial channel")

    def sendForce(self, force: TransformForce):
        msg = "*"
        msg = msg + str(force.get_x()) + ','
        msg = msg + str(force.get_y()) + ','
        msg = msg + str(force.get_rot()) + '#'

        to_forward = str.encode(msg)
        print(to_forward)

    def start(self):
        try:
            self.is_running = True
            self.channel = serial.Serial(self.com_port, self.baud_rate)
            self.thread = threading.Thread(target=self.loop, args=())
            self.thread.start()
        except:
            print("Failed to connect to gut, retrying after 3s")
            sleep(3)
            return self.start()
        # self.thread.join()

    def stop(self):
        self.is_running = False
        self.channel.close()


if __name__ == "__main__":
    x = SerialClient(comport="/dev/tty.usbmodem14101")
    x.start()

    print('asd')
