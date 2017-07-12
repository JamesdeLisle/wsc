import limits as lim
import space as sp
import RK as rk
import ldos
import uniform as uni
from multiprocessing import Pool, Manager
import time
import itertools

def worker( run_in ):
    
    U = uni.Uniform( run_in.getSet() ) 
    return { 'index' : run_in[ 'index' ], 'value' : U[ run_in[ 'func_str' ] ] }

if __name__ == '__main__':
        
    data_folder = 'data/'
    t0 = time.time()

    L = lim.Limits()
    P = sp.ParamSpace( L )

    run_time = time.strftime( '%Y%m%d%H%M' )
    
    for ( iT, T ), ( iE, E ) in itertools.product( enumerate( P.temp ), enumerate( P.energy ) ):
        
        P.initialiseData( ( iT, iE ) )
        strings = [ 'g_RET', 'g_KEL' ]
        DATA = dict()

        for string in strings:
            ti = time.time()
            print 'computing %s...' % ( string ) 
            run = P.getRun( iT, iE, string )
            p = Pool()
            DATA[ string ] = p.map( worker, run ) 
            p.close()
            print time.time() - ti
            
        for string in strings:
            P.updateData( DATA[ string ], string )

        del DATA

        P.writeData( '%s%s' % ( data_folder, run_time ) )
        print '#######--%d-%d--#######' % ( iT, iE )

    print 'Done!'

    print time.time() - t0


    ###################################

    #A = ldos.LDOS( P )
    #A.compute()
    #A.writeData( 'data/ldos.dat' )
