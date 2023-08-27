from os import path
from pydub import AudioSegment
from pathlib import Path
import subprocess
import ffmpeg
import numpy as np

PATH = Path(__file__).cwd()
SPC = PATH / "speech_recognition"
DDIR = SPC / "Dataset"

# # files                                                                    

# import required modules
dups = np.array([],dtype='S')
for get_dups in DDIR.glob("*.wav"):
    dups = np.append(dups, get_dups.name[:-3])

for get_file in DDIR.glob("*.mp3"): 
    if(get_file.name[:-3] not in dups):
        try : 
            subprocess.call(['ffmpeg', '-i', f'{DDIR}/{get_file.name}',
                            f'{DDIR}/{get_file.name[:-3]}wav'], shell=True)
            print(get_file.name)
        except Exception as e:
            print(e)

# convert mp3 to wav file