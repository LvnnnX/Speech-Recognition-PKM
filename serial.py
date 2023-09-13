from voice_recognition import *
import serial
from threading import Thread
import time
import concurrent.futures

# ser = serial.serial('/dev/tty.usbmodem14101', baudrate=9600)


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

def get_num():
    return 1


# with concurrent.futures.ThreadPoolExecutor() as executor:
#     while True:
#         run_voice = executor.submit(run_voice)
#         run_num = executor.submit(get_num)
        
#         print(run_voice.result())
while True:        
    Voice().start()
    time.sleep(3)
    print(value)

        
        
        

# time.sleep(3)
