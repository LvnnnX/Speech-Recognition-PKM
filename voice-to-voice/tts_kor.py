from gtts import gTTS
from io import BytesIO
from pygame import mixer
import time


text = '안녕하세요 소개합니다 제 이름은 Dito입니다'
# language = 'ru'

# myobj = gTTS(text=text, lang=language, slow=False)
# myobj.save(f'{DDIR}/PerkenalanDito.mp3')


def speak(text:str,lang:str):
    mp3_fp = BytesIO()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(mp3_fp)
    return mp3_fp

def start(text:str,language:str):
    mixer.init()
    sound = speak(text,language)
    sound.seek(0)
    mixer.music.load(sound, "mp3")
    mixer.music.play()
    time.sleep(5)

