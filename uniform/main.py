import limits as lim
import space as sp
import uniform as uni
from multiprocessing import Pool, Manager
import time
import itertools

class UniformMain:

    def __init__( self, start_time, data_folder ): 

        self.start_time = start_time
        self.data_folder = data_folder

    def run( self ):
        
        L = lim.Limits()
        P = sp.ParamSpace( L )

        for ( iT, T ), ( iE, E ) in itertools.product( enumerate( P.temp ), enumerate( P.energy ) ):
            
            P.initialiseData( ( iT, iE ) )
            strings = [ 'g_RET', 'g_KEL' ]
            DATA = dict()
            
            ######################################
            #runs = P.getRun( iT, iE, strings[1] )
            #for run in runs:
            #    X = worker( run )
            ######################################

            for string in strings:
                ti = time.time()
                print 'computing %s...' % ( string ) 
                run = P.getRun( iT, iE, string )
                p = Pool()
                DATA[ string ] = p.map( self.worker, run ) 
                p.close()
                print time.time() - ti
                
            for string in strings:
                P.updateData( DATA[ string ], string )

            del DATA

            P.writeData( '%s%s' % ( self.data_folder, self.start_time ) )
            print '#######--%d-%d--#######' % ( iT, iE )

        print 'Done!'

    def worker( run_in ):
    
        U = uni.Uniform( run_in.getSet() ) 
        return { 'index' : run_in[ 'index' ], 'value' : U[ run_in[ 'func_str' ] ] }
