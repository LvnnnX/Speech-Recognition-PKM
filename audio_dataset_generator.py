import os
from pathlib import Path
from tqdm import tqdm
import speech_recognition as sr
import pyaudio
import wave
import glob

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
all_type = ['maju','belok_kiri','belok_kanan','serong_kiri','serong_kanan','stop','putar_balik_kiri', 'putar_balik_kanan']

def check_file(path:str):
    os.getcwd()
    if not os.path.exists('dataset'):
        os.makedirs('dataset')

    if not os.path.exists(os.path.join('dataset', path)):
        os.makedirs(os.path.join('dataset', path))
    
    return os.chdir(os.path.join('dataset', path))

def check_latest_file(path:str):
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


generate('maju', 48)