import matplotlib.pyplot as plt
import gen.lim as lim
import numpy as np
from jsci.Coding import NumericDecoder
import json
import matplotlib


def dosline(path):
    font = {'family': 'normal',
            'weight': 'bold',
            'size': 9}
    matplotlib.rc('font', **font)
    lims = lim.Limits()
    lims.readData(path)
    with open(path, 'r') as f:
        content = json.loads(f.read(), cls=NumericDecoder)
        data = content['data']
    plt.plot(np.linspace(lims.energyMin, lims.energyMax, lims.nEnergy), data)
    plt.savefig('dos-total.pdf')
