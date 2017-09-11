from ana.unidos import LDOS
import os


data_folder = "data/"


def getFiles():

    return [f for f in os.listdir(data_folder)
            if os.path.isfile(os.path.join(data_folder, f)) and '-0-' in f]


files = sorted(getFiles())

for f in files:

    L = LDOS(f)
    print(L.compute())
