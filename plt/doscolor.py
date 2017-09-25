import matplotlib.pyplot as plt
import gen.lim as lim
import os
from jsci.Coding import NumericDecoder
import json
import numpy as np
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import scipy.interpolate
from matplotlib import ticker
from matplotlib import rc
import matplotlib


def getFiles(data_folder):

    return [os.path.join(data_folder, f) for f in os.listdir(data_folder)
            if os.path.isfile(os.path.join(data_folder, f)) and 'dos' in f]


def doscolor():
    data_folder = 'data/'
    files = sorted(getFiles(data_folder))
    lims = lim.Limits()
    lims.readData(files[0])
    x, y, z = [], [], []
    tSpace = np.linspace(lims.tempMin, lims.tempMax, lims.nTemp)
    eSpace = np.linspace(lims.energyMin, lims.energyMax, lims.nEnergy)

    for iT, T in enumerate(tSpace):
        with open(files[iT], 'r') as f:
            c = json.loads(f.read(), cls=NumericDecoder)
            for iE, E in enumerate(eSpace):
                x.append(T)
                y.append(E)
                z.append(c['data'][iE])

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
    rc('text', usetex=True)
    matplotlib.rcParams.update({'font.size': 52})

    fig = plt.figure(num=None, figsize=(8, 7), dpi=80)
    gs = gridspec.GridSpec(1, 1)
    ax1 = plt.subplot(gs[0])

    # Set up a regular grid of interpolation points
    xi, yi = np.linspace(x.min(),
                         x.max(),
                         300), np.linspace(y.min(), y.max(), 300)

    xi, yi = np.meshgrid(xi, yi)

    # Interpolate; also "nearest", "cubic" and others
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')

    im1 = ax1.imshow(zi,
                     vmin=z.min(),
                     vmax=z.max(),
                     origin='lower',
                     aspect='equal',
                     extent=[x.min(), x.max(), y.min(), y.max()])

    divider1 = make_axes_locatable(ax1)
    cax1 = divider1.append_axes('right', size='5%', pad=0.15)
    cbar = plt.colorbar(im1, cax=cax1)

    tick_locator = ticker.MaxNLocator(nbins=5)
    cbar.locator = tick_locator
    cbar.update_ticks()

    ax1.locator_params(axis='x', nbins=4)
    ax1.locator_params(axis='y', nbins=4)

    ax1.set_aspect('auto')
    ax1.set_xlabel(r"$\T$")
    ax1.set_ylabel(r"$\epsilon$", rotation='horizontal')
    ax1.yaxis.set_label_coords(-0.07, 0.7)

    plt.show()
