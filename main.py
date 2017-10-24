import gen.lim as lim
import gen.main as main
import time
import numpy as np
import os
from gen.parser import nameParser, getFiles


def clearup(data_folder):
    existingFiles = [f for f in os.listdir(data_folder)
                     if os.path.isfile(os.path.join(data_folder, f))]
    if existingFiles:
        os.mkdir(os.path.join(data_folder, existingFiles[0][0:14]))
        for f in existingFiles:
            os.rename(os.path.join(data_folder, f),
                      os.path.join(data_folder, existingFiles[0][0:14], f))


def Main(string, partial=False):

    data_folder = 'data/'
    if partial:
        files = getFiles(['0'], 'up', data_folder, 'raw')
        if files['0']:
            run_time = nameParser(files['0'][0], 'run')
        else:
            run_time = time.strftime('%Y%m%d%H%M%S')
    else:
        clearup(data_folder)
        run_time = time.strftime('%Y%m%d%H%M%S')


    L = lim.Limits()
    L.spinDir = string
    L.nEnergy = 10
    L.nKPolar = 10
    L.nKAzimu = 10
    L.nTemp = 1
    L.nAlpha = 2
    L.energyMin = -3.0
    L.energyMax = 3.0
    L.kPolarMin = 0.0
    L.kPolarMax = np.pi
    L.kAzimuMin = 0.0
    L.kAzimuMax = 2 * np.pi
    L.T_c = 0.1
    L.tempMin = 0.02
    L.tempMax = 0.02
    L.tempInc = 1.0 / 50.0
    L.alphaMin = -6.0
    L.alphaMax = 0.0
    L.a1 = 0.135
    L.a2 = 0.22
    L.a3 = 0.48
    L.a4 = -0.242
    L.B_z = 0.1
    L.tau = 0.01
    L.finalise()
    L.saveToFile(run_time)

    orders = ['0', '1', '2', '3']
    for order in orders:
        M = main.Main(L, run_time, data_folder, order)
        M.run()


if __name__ == '__main__':

    strings = ['up', 'dn']
    for string in strings:
        Main(string, partial=True)
