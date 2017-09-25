import matplotlib.pyplot as plt
import gen.lim as lim
import numpy as np
from jsci.Coding import NumericDecoder
import json


def dosline(path):
    lims = lim.Limits()
    lims.readData(path)
    with open(path, 'r') as f:
        content = json.loads(f.read(), cls=NumericDecoder)
        data = content['data']
    plt.plot(np.linspace(lims.energyMin, lims.energyMax, lims.nEnergy), data)
    plt.show()
