import uni.uniform as unif
import ret.retarded as reta
import gen.lim as lim
import time
import numpy as np

L = lim.Limits()
L.spinDir = 'up'
L.nEnergy = 100
L.nKPolar = 100
L.nKAzimu = 100
L.nTemp = 100
L.nAlpha = 100
L.energyMin = -6.0
L.energyMax = 6.0
L.kPolarMin = 0.0
L.kPolarMax = np.pi
L.kAzimuMin = 0.0
L.kAzimuMax = 2 * np.pi
L.T_c = 0.1
L.tempMin = 0.001
L.tempMax = 0.1
L.tempInc = 1.0 / 200.0
L.alphaMin = -6.0
L.alphaMax = 6.0
L.a1 = 0.3
L.a2 = -0.13
L.a3 = 0.15
L.a4 = 0.34
L.B_z = 1.0
L.finalise()

if True:
    run_time = time.strftime('%Y%m%d%H%M')
    data_folder = 'data/'
    U = unif.UniformMain(L, run_time, data_folder)
    U.run()
    #R = reta.RetardedMain(L, run_time, data_folder)
    #R.run()

if False:
    run_time = '201707141153'
    data_folder = 'data/'
    L = lim.Limits()
    R = reta.RetardedMain(L, run_time, data_folder)
    R.run()
