from ana.unidos import LDOS
from gen.lim import Limits
import os
import numpy as np
from jsci.Coding import NumericEncoder
import json

data_folder = "data/"


def getFiles():

    return [os.path.join(data_folder, f) for f in os.listdir(data_folder)
            if os.path.isfile(os.path.join(data_folder, f)) and '-0-' in f]


files = sorted(getFiles())
lims = Limits()
lims.readData(files[0])

for i in range(lims.nTemp):
    data = np.zeros(lims.nTemp)
    for j in range(lims.nEnergy):
        k = j + i * lims.nTemp
        L = LDOS(files[k], '0', 'gR')
        data[j] = np.abs(L.compute())
    path = files[k][0:-4] + '-udos'
    with open(path, 'w') as f:
        f.write(json.dumps({'param': L.lim.save(),
                            'data': data},
                           cls=NumericEncoder,
                           indent=4,
                           sort_keys=True))
