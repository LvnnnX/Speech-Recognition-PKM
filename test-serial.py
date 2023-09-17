from voice_recognition import *
from threading import Thread
import time
import serial
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

# ser = serial.serial('/dev/tty.usbmodem14101', baudrate=9600)
serialInst.baudrate = 115200
serialInst.port = "COM3"
serialInst.open()

if not os.path.exists(os.path.join(ROOT, 'tmp')):
    os.mkdir(os.path.join(ROOT, 'tmp'))
os.chdir(os.path.join(ROOT, 'tmp'))

value = 0

class Voice(Thread):
    def run(self):
        global value
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print(f"Recording...")
        FRAMES = []
        seconds = 3
        for i in range(0, int(RATE / CHUNK * seconds)):
            data = stream.read(CHUNK)
            FRAMES.append(data)
            
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(f'data.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(FRAMES))
        wf.close()
        value =  key_list[val_list.index(predict()[0])]


class sendSerial(Thread):
    def run(self):
        global value
        try:
            while True:
                data_to_send = input("Enter data to send to ESP32: ")
                serialInst.write(data_to_send.encode())  # Send data to ESP32
                received_data = serialInst.readline().decode().strip()  # Read data from ESP32
                print("Received from ESP32:", received_data)

        except KeyboardInterrupt:
            pass
            # serialInst.close()  # Close the serial port when the script is interrupted
        # time.sleep(3)
        # value = 0
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     while True:
#         run_voice = executor.submit(run_voice)
#         run_num = executor.submit(get_num)
        
#         print(run_voice.result())
while True:        
    Voice().start()
    time.sleep(3)
    sendSerial().start()
    
    

        
        
        

# time.sleep(3)
