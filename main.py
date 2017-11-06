import gen.lim as lim
import gen.main as main
import time
import numpy as np
import os
from gen.parser import nameParser, getFiles
import sys


def clearup(df):
    # TODO Outdated fuction.
    existingFiles = [f for f in os.listdir(df)
                     if os.path.isfile(os.path.join(df, f))]
    if existingFiles:
        os.mkdir(os.path.join(df, existingFiles[0][0:14]))
        for f in existingFiles:
            os.rename(os.path.join(df, f),
                      os.path.join(df, existingFiles[0][0:14], f))


def getRunTime(partial, df):
    if partial:
        files = getFiles(['0'], 'up', df, 'raw')
        if files['0']:
            rt = nameParser(files['0'][0], 'run')
        else:
            rt = time.strftime('%Y%m%d%H%M%S')
    else:
        clearup(df)
        rt = time.strftime('%Y%m%d%H%M%S')
    return rt


def Main(string, B_z, tempInc, rtval=0, partial=False):

    df = 'data/'
    if rtval == 0:
        rt = getRunTime(partial, df)
    else:
        rt = rtval

    L = lim.Limits()
    L.spinDir = string
    L.nEnergy = 50
    L.nKPolar = 25
    L.nKAzimu = 50
    L.nTemp = 1
    L.nAlpha = 50
    L.energyMin = -1.0
    L.energyMax = 1.0
    L.kPolarMin = 0.0
    L.kPolarMax = np.pi
    L.kAzimuMin = 0.0
    L.kAzimuMax = 2 * np.pi
    L.T_c = 0.1
    L.tempMin = 0.02
    L.tempMax = 0.02
    L.tempInc = tempInc
    L.alphaMin = -3.0
    L.alphaMax = 0.0
    L.a1 = 0.135
    L.a2 = 0.22
    L.a3 = 0.48
    L.a4 = -0.242
    L.B_z = B_z
    L.tau = 0.01
    L.vU = 1.0
    L.vD = 0.75
    L.finalise()
    L.saveToFile(rt)

    t0 = time.time()
    orders = ['0', '1', '2', '3', '4', '5']
    for order in orders:
        M = main.Main(L, rt, df, order)
        M.run()
    print 'Time taken: %d' % (time.time() - t0)


if __name__ == '__main__':

    par_val = True
    spin = sys.argv[1]
    B_z = float(sys.argv[2])
    tempInc = float(sys.argv[3])
    if sys.argv:
        print sys.argv
        Main(spin, B_z, tempInc, partial=par_val)
    else:
        print 'Misssing argv.'
