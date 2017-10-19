import matplotlib.pyplot as plt
import gen.lim as lim
import numpy as np
from jsci.Coding import NumericDecoder
import json
import matplotlib
from gen.parser import nameParser


def dosline(path, filename):
    font = {'weight': 'bold',
            'size': 12}
    matplotlib.rc('font', **font)
    matplotlib.rc('text', usetex=True)
    lims = lim.Limits()
    lims.readData(path)
    lims.finalise()
    with open(path, 'r') as f:
        content = json.loads(f.read(), cls=NumericDecoder)
        data = content['data']

    plt.plot(np.linspace(lims.energyMin, lims.energyMax, lims.nEnergy), data)
    plt.ylim((0.0, 1.0))
    plt.xlim((lims.energyMin, lims.energyMax))
    plt.ylabel(r'$\rho(\epsilon)$')
    plt.xlabel(r'$\epsilon$')
    plt.title(r'$DOS-%s-%s$' % (filename,lims.spinDir))
    ypos = 3 * plt.ylim()[1] / 4
    xpos = 3 * plt.xlim()[1] / 4
    shift = plt.ylim()[1] / 20
    plt.text(xpos, ypos, r'$\gamma=%.2f$' % lims.gamma1)
    plt.text(xpos, ypos - shift, r'$\bar{\gamma}=%.2f$' % lims.gamma2)
    plt.text(xpos, ypos - 2 * shift, r'$B_{z}=%.2f$' % lims.B_z)
    plt.text(xpos, ypos - 3 * shift, r'$\tau^{-1}=%.2f$' % lims.tau)
    plt.text(xpos, ypos - 4 * shift, r'$T=%.2f$' % lims.tempMin)
    plt.text(xpos, ypos - 5 * shift, r'$T_{c}=%.2f$' % lims.T_c)
    maxdel = (1.764 / (2 * np.pi))
    maxdel *= np.tanh(np.sqrt(lims.T_c / 0.02 - 1.0))
    mindel = maxdel * min(np.abs([lims.gamma1, lims.gamma2]))
    maxdel *= max(np.abs([lims.gamma1, lims.gamma2]))
    plt.axvline(x=maxdel, linestyle='dashed', color='black')
    plt.axvline(x=-maxdel, linestyle='dashed', color='black')
    plt.axvline(x=mindel, linestyle='dashed', color='black')
    plt.axvline(x=-mindel, linestyle='dashed', color='black')
    plt.savefig('pdf/dos-%s-%s.pdf' % (filename, lims.spinDir))
    plt.close()
