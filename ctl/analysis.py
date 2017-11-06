from ana.unidos import LDOS
import ana.unidostotal as LDOST
from gen.lim import Limits
import numpy as np
from jsci.Coding import NumericEncoder, NumericDecoder
import json
import sys
from os import getcwd, remove
from os.path import join
from gen.parser import nameParser, getFiles
from ana.heatcurrent import HCOND
from ana.magnetisation import MAG
import itertools
import time


data_folder = join(getcwd(), "data/")


def compIndiDOS(orders, files, lims):
    print 'Computing DOS...'
    for iT in range(lims.nTemp):
        data = {order: np.zeros(lims.nEnergy) for order in orders}
        for iE in range(lims.nEnergy):
            index = iE + iT * lims.nEnergy
            perc = 100 * float(index) / (lims.nEnergy * lims.nTemp)
            sys.stdout.write('\r%.2f%%' % perc)
            sys.stdout.flush()
            L = {order: LDOS(files[order][index], order, 'gR')
                 for order in orders}
            for order in orders:
                data[order][iE] = np.abs(L[order].compute())
        path = {order: join(data_folder,
                            nameParser(files[order][index],
                                       'run+order+spin+temp'))
                + '-dos' for order in orders}
        for order in orders:
            with open(path[order], 'w') as f:
                f.write(json.dumps({'param': lims.save(),
                                    'data': data[order]},
                                   cls=NumericEncoder,
                                   indent=4,
                                   sort_keys=True))
    sys.stdout.write('\rDone!    \n')
    sys.stdout.flush()


def compTotalDOS(files, lims):
    print 'Computing DOS...'
    for iT in range(lims.nTemp):
        data = np.zeros(lims.nEnergy)
        for iE in range(lims.nEnergy):
            index = iE + iT * lims.nEnergy
            perc = 100 * float(index) / (lims.nEnergy * lims.nTemp)
            sys.stdout.write('\r%.2f%%' % perc)
            sys.stdout.flush()
            L = LDOST.LDOS(files['0'][index], files['2'][index])
            data[iE] = np.abs(L.compute())
        path = join(data_folder,
                    nameParser(files['0'][index], 'run')
                    + '-total'
                    + nameParser(files['0'][index], 'spin+temp')
                    + '-dos')
        with open(path, 'w') as f:
            f.write(json.dumps({'param': lims.save(),
                                'data': data},
                               cls=NumericEncoder,
                               indent=4,
                               sort_keys=True))
    sys.stdout.write('\rDone!    \n')
    sys.stdout.flush()


def Main():
    orders = ['0', '2']
    files = getFiles(orders, data_folder, 'raw')
    lims = Limits()
    lims.loadFromFile(data_folder)
    compIndiDOS(orders, files, lims)
    compTotalDOS(files, lims)


def generateStore(sf, nb, nt):
    dat = {'b': [], 't': [], 'M': []}
    with open(join(df, 'DAT'), 'w') as f:
        f.write(json.dumps(dat, cls=NumericEncoder, indent=4, sort_keys=True))


def updateStore(sf, b, t, val):
    with open(join(df, 'DAT'), 'r') as f:
        dat = json.loads(f.read(), cls=NumericDecoder)
    dat['b'].append(b)
    dat['t'].append(t)
    dat['M'].append(val)
    with open(join(df, 'DAT'), 'w') as f:
        f.write(json.dumps(dat, cls=NumericEncoder, indent=4, sort_keys=True))


def checkREG(df, iB, it):
    with open(join(df, 'REG'), 'r') as f:
        REG = json.loads(f.read(), cls=NumericDecoder)['reg']
    return all([REG[iB][it]['up'], REG[iB][it]['dn']])


def updateREG(df, pt, iB, it):
    with open(join(df, 'REG'), 'r') as f:
        REG = json.loads(f.read(), cls=NumericDecoder)['reg']
    REG[iB][it][pt] = True
    with open(join(df, 'REG'), 'w') as f:
        f.write(json.dumps({'reg': REG},
                           cls=NumericEncoder,
                           indent=4))


def generateREG(df, nb, nt):
    reg = [[{'up': False,
             'dn': False,
             'an': False}
            for i in range(nb)] for j in range(nt)]
    with open(join(df, 'REG'), 'w') as f:
        f.write(json.dumps({'reg': reg},
                           cls=NumericEncoder,
                           indent=4))


if __name__ == '__main__':
    sf = 'store/'
    df = 'data/'
    nb = 50
    nt = 50
    bmin = 0.0
    bmax = 0.3
    tmin = 0.0
    tmax = 0.03
    bSpace = np.linspace(bmin, bmax, nb)
    tSpace = np.linspace(tmin, tmax, nt)
    generateStore(sf, nb, nt)
    generateREG(df, nb, nt)
    DOF = itertools.product(enumerate(bSpace), enumerate(tSpace))
    pre = (0, 0)
    orders = ['0', '1', '2', '3', '4', '5']
    for (ib, b), (it, t) in DOF:
        while not checkREG(df, ib, it):
            time.sleep(5)
        M = MAG('data/', ['5'])
        updateStore(sf, b, t, M.compute())
        flsup = getFiles(orders, 'up', df, 'raw')
        flsdn = getFiles(orders, 'dn', df, 'raw')
        for order in orders:
            for fup, fdn in zip(flsup[order], flsdn[order]):
                remove(fup)
                remove(fdn)
        updateREG(df, 'an', ib, it)
