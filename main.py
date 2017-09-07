import gen.lim as lim
import uni.uniform as unif
import ret.retarded as reta
import kel.keldysh as keld
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
    L.nEnergy = 10
    L.nKPolar = 10
    L.nKAzimu = 10
    L.nTemp = 1
    L.nAlpha = 10
    L.energyMin = -6.0
    L.energyMax = 6.0
    L.kPolarMin = 0.000001
    L.kPolarMax = np.pi
    L.kAzimuMin = 0.000001
    L.kAzimuMax = 2 * np.pi
    L.T_c = 0.1
    L.tempMin = 0.08
    L.tempMax = 0.08
    L.tempInc = 1.0 / 200.0
    L.alphaMin = -6.0
    L.alphaMax = 6.0
    L.a1 = 0.3
    L.a2 = -0.13
    L.a3 = 0.15
    L.a4 = 0.34
    L.B_z = 1.0
    L.finalise()

    U = unif.UniformMain(L, run_time, data_folder)
    U.run()
    R = reta.RetardedMain(L, run_time, data_folder)
    R.run()
    K = keld.KeldyshMain(L, run_time, data_folder)
    K.run()
