import os
from pathlib import Path
from tqdm import tqdm

PATH = Path(__file__).parent
DATASET = PATH / 'dataset'


listdirs = [f for f in os.listdir(DATASET) if os.path.isdir(os.path.join(DATASET, f))]

# for dirs in tqdm(listdirs):
dirs = 'other'
listfiles = [f for f in os.listdir(os.path.join(DATASET, dirs)) if os.path.isfile(os.path.join(DATASET, dirs, f))]
# print(listfiles)
for num,files in enumerate(listfiles):
    os.rename(os.path.join(DATASET, dirs, files), os.path.join(DATASET, dirs, dirs+'_'+str(num)+'.wav'))
    # print(files)
    # pass
    # break
    
