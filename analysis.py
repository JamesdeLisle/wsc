from ana.unidos import LDOS
import os
import numpy as np
from jsci.Coding import NumericEncoder
import json

data_folder = "data/"


def getFiles():

    return [os.path.join(data_folder, f) for f in os.listdir(data_folder)
            if os.path.isfile(os.path.join(data_folder, f)) and '-0-' in f]


files = sorted(getFiles())
data = np.zeros(len(files))

count = 0
for f in files:

    L = LDOS(f)
    data[count] = L.compute()
    count += 1

path = os.path.join(data_folder, files[0][0:13])
path_complete = path + '-0-dos'
with open(path_complete, 'w') as f:
    f.write(json.dumps({'param': L.lim.save(),
                        'data': data},
                       cls=NumericEncoder,
                       indent=4,
                       sort_keys=True))
