import gen.lim as lim
import gen.main as main
import time
import numpy as np
import os


def clearup(data_folder):
    existingFiles = [f for f in os.listdir(data_folder)
                     if os.path.isfile(os.path.join(data_folder, f))]
    if existingFiles:
        os.mkdir(os.path.join(data_folder, existingFiles[0][0:12]))
        for f in existingFiles:
            print os.path.join(data_folder, existingFiles[0][0:12], f)
            os.rename(os.path.join(data_folder, f),
                      os.path.join(data_folder, existingFiles[0][0:12], f))


if __name__ == '__main__':

    data_folder = 'data/'
    run_time = time.strftime('%Y%m%d%H%M%S')

    clearup(data_folder)

    L = lim.Limits()
    L.spinDir = 'up'
    L.nEnergy = 10000
    L.nKPolar = 50
    L.nKAzimu = 100
    L.nTemp = 1
    L.nAlpha = 1
    L.energyMin = -0.02
    L.energyMax = -1e-6
    L.kPolarMin = 1e-6
    L.kPolarMax = np.pi
    L.kAzimuMin = 1e-6
    L.kAzimuMax = 2 * np.pi
    L.T_c = 0.1
    L.tempMin = 0.02
    L.tempMax = 0.02
    L.tempInc = 1.0 / 200.0
    L.alphaMin = -6.0
    L.alphaMax = 6.0
    L.a1 = 0.1
    L.a2 = -0.06
    L.a3 = 0.12
    L.a4 = 0.05
    L.B_z = 0.1
    L.tau = 0.0000001
    L.finalise()

    orders = ['0', '1']
    for order in orders:
        M = main.Main(L, run_time, data_folder, order)
        M.run()
