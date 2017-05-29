import limits as lim
import space as sp
import RK as rk
import ldos
from multiprocessing import Pool, Manager
import time
import itertools


t0 = time.time()

L = lim.Limits()
P = sp.ParamSpace( L )

def worker( run_in ):

    motile = rk.RK( run_in )
    motile.doRK()
    return { 'index' : run_in[ 'index' ], 'value' : motile.getValue() }

strings = [ 'GAM_R_F', 'GAM_R_B' ]
DATA = dict()

for ( iT, T ), ( iE, E ) in itertools.product( enumerate( P.temp ), enumerate( P.energy ) ):

    for string in strings:
        print 'computing %s...' % ( string ) 
        run = P.getRun( iT, iE, string )
        p = Pool()
        DATA[ string ] = p.map( worker, run ) 
        print time.time() - t0

    for string in strings:
        P.updateData( DATA[ string ], string )

    del DATA
    DATA = dict()

    strings = [ 'DIST_F', 'DIST_B' ]

    for string in strings:
        print 'computing %s...' % ( string ) 
        run = P.getRun( iT, iE, string )
        p = Pool()
        DATA[ string ] = p.map( worker, run ) 
        print time.time() - t0

    for string in strings:
        P.updateData( DATA[ string ], string )

print 'Done!'

print time.time() - t0

P.writeData( 'data/gdata.dat' )

###################################

A = ldos.LDOS( P )
A.compute()
A.writeData( 'data/ldos.dat' )
