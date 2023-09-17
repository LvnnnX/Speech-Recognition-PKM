import os
from pathlib import Path
from tqdm import tqdm
import speech_recognition as sr
import pyaudio
import wave
import glob
import librosa
import pandas as pd
import numpy as np
import pickle


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
ROOT = os.getcwd()

all_type = ['maju','belok_kiri','belok_kanan','serong_kiri','serong_kanan','stop','putar_balik_kiri', 'putar_balik_kanan']

model = pickle.load(open(os.path.join('model','svm_model_speech_recognition.pkl'), 'rb'))

scaler = pickle.load(open(os.path.join('model','svm_scaler_speech_recognition.pkl'), 'rb'))

maps = {
    'maju': 0,
    'belok_kiri': 1,
    'belok_kanan': 2,
    'serong_kiri': 3,
    'serong_kanan': 4,
    'stop': 5,
    'putar_balik_kiri': 6,
    'putar_balik_kanan': 7,
    'other': 8
}

key_list = list(maps.keys())
val_list = list(maps.values())

def mfcc(audio_obj:str=None, frame_rate:int=2048, hop_len:int=512, mfcc_num:int=100):
    signal, sr = librosa.load(audio_obj)
    mfcc_spectrum = librosa.feature.mfcc(y=signal, sr=sr, n_fft=frame_rate, hop_length=hop_len, n_mfcc=mfcc_num)
    # delta_1_mfcc = librosa.feature.delta(mfcc_spectrum, order=1)
    # delta_2_mfcc = librosa.feature.delta(mfcc_spectrum, order=2)

    mfcc_features = np.mean(mfcc_spectrum, axis=1)
    return mfcc_features

def audio_features(path:os.PathLike=None, frame_size:int=2048, hop_len:int=512, mfcc_num:int=100):
    audios_mfcc = []
    
    mfcc_score = mfcc(audio_obj=path, frame_rate=frame_size, hop_len=hop_len, mfcc_num=mfcc_num)
    audios_mfcc.append(mfcc_score)

    audio_features = np.column_stack(audios_mfcc)
    df = pd.DataFrame(audio_features)
    df = df.T

    return df

def predict():
    df = audio_features(path=os.path.join(ROOT, 'tmp', 'data.wav'))
    df = scaler.transform(df)
    y_pred = model.predict(df)
    return y_pred

def main():
    if not os.path.exists(os.path.join(ROOT, 'tmp')):
        os.mkdir(os.path.join(ROOT, 'tmp'))
    os.chdir(os.path.join(ROOT, 'tmp'))
    while True:
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
        
        try:
            values = predict()[0].tolist()
            values = values.index(max(values))
            print(key_list[val_list.index(values)])
        # print(values)
        except:
            print(key_list[val_list.index(predict()[0])])
        
if __name__ == '__main__':
    main()