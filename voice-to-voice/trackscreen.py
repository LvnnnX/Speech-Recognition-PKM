import time
from PIL import ImageGrab  # screenshot
import pyautogui as pg
import pytesseract
from pytesseract import Output
from pydub import AudioSegment
from pydub.playback import play
from pathlib import Path
from pyfirmata import Arduino

PATH = Path(__file__).parent.parent
VDIR = PATH / 'Dataset'

pytesseract.pytesseract.tesseract_cmd = (r"C:\Program Files\Tesseract-OCR\tesseract.exe") # needed for Windows as OS
board = Arduino('COM3')

def get_phantom_data():
    phantom_buy_status = ImageGrab.grab(bbox=(800,540,855,560))
    phantom_gray = phantom_buy_status.convert('L')
    data=pytesseract.image_to_boxes(phantom_gray,output_type=Output.DICT)
    try:
        text=''.join(data['char'])
        if(text=='OWNED'):
            sound = AudioSegment.from_mp3(f'{VDIR}/kerjabagus.mp3')
            play(sound)
        else:
            return
    except:
        pass


def get_hp(hp_stats,next_hp):
    hp_status = ImageGrab.grab(bbox=(570,1000,650,1050))
    hp_gray = hp_status.convert('L')
    hp_data = pytesseract.image_to_boxes(hp_gray, output_type=Output.DICT)
    try:
        text = ''.join(hp_data['char'])
        if(hp_stats!=int(text)):
            if(int(text)<=50):
                sound = AudioSegment.from_mp3(f'{VDIR}/akubutuhmedkit.mp3')
                play(sound)
                board.digital[13].write(1)
                time.sleep(2)
                board.digital[13].write(0)
                print(f'hp_stats = {hp_stats}, hp = {int(text)}')
                return int(text)
            else:
                return 999
    except:
        return 999
    return 999

hp_stats = 0
next_hp = 0
while True:
    time.sleep(0.5)
    # screen =  ImageGrab.grab(bbox=(886,1073,1286,1173))  # screenshot
    mouse_pos = pg.position()
    # print(f'mouse pos : {mouse_pos}')
    next_hp = get_hp(hp_stats,next_hp)
    if(next_hp!=999):
        if(hp_stats!=next_hp):
            # print('shocked!')
            hp_stats=next_hp
            # print(f'hp_stats : {hp_stats}')
    get_phantom_data()
    # screen = ImageGrab.grab(bbox=(mouse_pos[0],mouse_pos[1],mouse_pos[0]+400,mouse_pos[1]+200))
    # screen = ImageGrab.grab(bbox=(570,1000,650,1050))
    # phantom_buy_status = ImageGrab.grab(bbox=(800,540,855,560))
    # cap = screen.convert('L')   # make grayscale
    # phantom_gray = phantom_buy_status.convert('L')

    # screen.show()
    # data=pytesseract.image_to_boxes(cap,output_type=Output.DICT)
    # try:
    #     text = ''.join(data['char'])
    #     if(text=='OWNED'):
    #         sound = AudioSegment.from_mp3(f'{VDIR}/kerjabagus.mp3')
    #         play(sound)
    #     print(text)

    # except Exception as e:
    #     # print(e)
    #     pass