import limits as lim
import space as sp
import RK as rk
import ldos
from multiprocessing import Pool
import time
import numpy as np

L = lim.Limits()
P = sp.ParamSpace( L )
P_b = sp.ParamSpace( L )


string = [ 'DIST_F', 'DIST_B' ]

run = P.getRun( string[1] )
for x in run:
    
    motile = rk.RK( x )
    motile.doRK()



