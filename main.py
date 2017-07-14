import uni.uniform as unif
import ret.retarded as reta
import gen.lim as lim
import time

run_time = time.strftime( '%Y%m%d%H%M' )
data_folder = 'data/'
L = lim.Limits()
U = unif.UniformMain( L, run_time, data_folder )
U.run()
R = reta.RetardedMain( L, run_time, data_folder )
R.run()



