import os
from pathlib import Path
from tqdm import tqdm
import speech_recognition as sr
import pyaudio
import wave
import glob
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
ROOT = os.getcwd()
all_type = ['maju','belok_kiri','belok_kanan','serong_kiri','serong_kanan','stop','putar_balik_kiri', 'putar_balik_kanan', 'other']

def check_file(path:str):
    if not os.path.exists(os.path.join(ROOT, 'dataset')):
        os.makedirs('dataset')

    if not os.path.exists(os.path.join(ROOT, 'dataset', path)):
        os.makedirs(os.path.join(ROOT, 'dataset', path))
    
    return os.chdir(os.path.join(ROOT, 'dataset', path))

def check_latest_file(path:str):
    os.chdir(os.path.join(ROOT, 'dataset', path))
    list_of_files = glob.glob('*.wav')
    return len(list_of_files)

def generate(type:str, many:int=1):
    check_file(type)
    start_num = check_latest_file(type)
    for x in range(many):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print(f"Recording for {type.upper()}...")
        FRAMES = []
        seconds = 3
        for i in range(0, int(RATE / CHUNK * seconds)):
            data = stream.read(CHUNK)
            FRAMES.append(data)
            
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(f'{type}_{start_num + x+1}.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(FRAMES))
        wf.close()
        
        print(f"Saved as {type}_{start_num + x+1}.wav")


for type in ['other']:
    if input('Start? y/n').lower() == 'y':
        print(f'Get ready to record {type} ...')
        for i in range(3):
            print(3-i, end=' ')
            time.sleep(1)
        print()
        generate(type, 50)
    else:
        break