import uni.uniform as unif
import ret.retarded as reta
import gen.lim as lim
import time


if False:
    run_time = time.strftime('%Y%m%d%H%M')
    data_folder = 'data/'
    L = lim.Limits()
    U = unif.UniformMain(L, run_time, data_folder)
    U.run()
    R = reta.RetardedMain(L, run_time, data_folder)
    R.run()

if True:
    run_time = '201707141153'
    data_folder = 'data/'
    L = lim.Limits()
    R = reta.RetardedMain(L, run_time, data_folder)
    R.run()
