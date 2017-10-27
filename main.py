import gen.lim as lim
import gen.main as main
import time
import numpy as np
import os
from gen.parser import nameParser, getFiles
import sys


def clearup(data_folder):
    existingFiles = [f for f in os.listdir(data_folder)
                     if os.path.isfile(os.path.join(data_folder, f))]
    if existingFiles:
        os.mkdir(os.path.join(data_folder, existingFiles[0][0:14]))
        for f in existingFiles:
            os.rename(os.path.join(data_folder, f),
                      os.path.join(data_folder, existingFiles[0][0:14], f))


def getRunTime(partial, data_folder):
    if partial:
        files = getFiles(['0'], 'up', data_folder, 'raw')
        if files['0']:
            run_time = nameParser(files['0'][0], 'run')
        else:
            run_time = time.strftime('%Y%m%d%H%M%S')
    else:
        clearup(data_folder)
        run_time = time.strftime('%Y%m%d%H%M%S')
    return run_time


def Main(string, partial=False):

    data_folder = 'data/'
    run_time = getRunTime(partial, data_folder)

    L = lim.Limits()
    L.spinDir = string
    L.nEnergy = 100
    L.nKPolar = 50
    L.nKAzimu = 100
    L.nTemp = 1
    L.nAlpha = 100
    L.energyMin = -1.0
    L.energyMax = 1.0
    L.kPolarMin = 0.0
    L.kPolarMax = np.pi
    L.kAzimuMin = 0.0
    L.kAzimuMax = 2 * np.pi
    L.T_c = 0.1
    L.tempMin = 0.02
    L.tempMax = 0.02
    L.tempInc = 1.0 / 50.0
    L.alphaMin = -3.0
    L.alphaMax = 0.0
    L.a1 = 0.135
    L.a2 = 0.22
    L.a3 = 0.48
    L.a4 = -0.242
    L.B_z = 0.1
    L.tau = 0.01
    L.vU = 1.0
    L.vD = 0.75
    L.finalise()
    L.saveToFile(run_time)

    orders = ['0', '1', '2', '3', '4', '5']
    for order in orders:
        M = main.Main(L, run_time, data_folder, order)
        M.run()


if __name__ == '__main__':

    par_val = True
    if sys.argv:
        print sys.argv
        Main(sys.argv[1], partial=par_val)
    else:
        strings = ['up', 'dn']
        for string in strings:
            Main(string, partial=par_val)
