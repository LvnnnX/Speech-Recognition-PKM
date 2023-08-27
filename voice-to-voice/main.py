import speech_recognition as sr
import os
from openai_connector import chatgpt
import tts_kor
from mtranslate import translate
from pathlib import Path

PATH = Path(__file__).parent.parent
DDIR = PATH / "Dataset"


engine=sr.Recognizer()
mic = sr.Microphone(1)
title = 'BANG UDAH BANG'
from_file = sr.AudioFile(f'{DDIR}/{title}.wav')

def call():
    # with mic as source:
    with from_file as source:
        engine.adjust_for_ambient_noise(source)
        rekaman = engine.record(source) #kalo pake from_file

        # print('--=-- Mulai --=--')
        # rekaman = engine.listen(source) #kalo pake mic
        # print('--=-- Selesai --=--')
        
            # BY GOOGLE #
        hasil=engine.recognize_google(rekaman,language='id-ID')
        en_ = translate(str(hasil),'ko','auto')
        # print(type(hasil))
        # os.system('cls')
        print(f'Idn : {hasil}')
        print(f'Kor : {en_}')
        tts_kor.start(en_,'ko')
            
            # END BY GOOGLE #


# while(True):
#     # if input("Mulai voice recognition?(y/n)") == 'y':
#     #     call()
#     # else:
#     #     break
call()