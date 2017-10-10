from ana.unidos import LDOS
from gen.lim import Limits
import os
import numpy as np
from jsci.Coding import NumericEncoder
import json

data_folder = "data/"


def getFiles(order):

    return [os.path.join(data_folder, f) for f in os.listdir(data_folder)
            if os.path.isfile(os.path.join(data_folder, f)) and '-%d-' % (order) in f]

files = {}
files['0'] = sorted(getFiles(0))
files['1'] = sorted(getFiles(1))
lims = Limits()
lims.readData(files['0'][0])

for i in range(lims.nTemp):
    data = np.zeros(lims.nEnergy)
    for j in range(lims.nEnergy):
        k = j + i * (lims.nEnergy)
        print k
        print files['0'][k]
        L = LDOS(files['0'][k], '0', 'gR')
        data[j] = np.abs(L.compute())
        print data[j]
    path = files['0'][k][0:-5] + '-udos'
    with open(path, 'w') as f:
        f.write(json.dumps({'param': L.lim.save(),
                            'data': data},
                           cls=NumericEncoder,
                           indent=4,
                           sort_keys=True))
