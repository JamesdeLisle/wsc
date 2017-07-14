import itertools
import numpy as np
from jsci.Coding import NumericEncoder, NumericDecoder
import json
import os

class RunContainer:

    def __init__( self, index, temperature, energy, Alpha, k_polar, k_azimuthal, constants, data ):
        
        self.store = dict()
        self.store[ 'index' ] = index
        self.store[ 'temperature' ] = temperature
        self.store[ 'energy' ] = energy
        self.store[ 'k_polar' ] = k_polar
        self.store[ 'k_azimuthal' ] = k_azimuthal 
        self.store[ 'Alpha' ] = Alpha
        self.store[ 'constants' ] = constants
        self.store[ 'data' ] = data

    def __getitem__( self, key ):
        
        return self.store[ key ]
   
    def getSet( self ):
        
        keys = [ 'temperature', 'energy', 'k_polar', 'k_azimuthal', 'constants', 'Alpha' ]

        return dict( dict( ( key, self.store[ key ] ) for key in keys ), **self.getTransSpace() )

    def getTransSpace( self ):
        
        x = self.store[ 'Alpha' ] * np.sin( self.store[ 'k_polar' ] ) * np.cos( self.store[ 'k_azimuthal' ] ) 
        y = self.store[ 'Alpha' ] * np.sin( self.store[ 'k_polar' ] ) * np.sin( self.store[ 'k_azimuthal' ] ) 
        z = self.store[ 'Alpha' ] * np.cos( self.store[ 'k_polar' ] ) 
        
        return { 'R_now' : np.sqrt( x * x + y * y ), 'P_now' : np.arctan2( y, x ), 'Z_now' : self.store[ 'Alpha' ] * np.cos( self.store[ 'k_polar' ] ) }

class ParamSpace:

    def __init__( self, limits, data_folder, run_time ):
        
        """defines the parameter space"""
        self.limits = limits
        self.constants = self.limits.getConstants()
        
        self.data_folder = data_folder
        self.run_time = run_time

        self.temp           = np.linspace( limits[ 'temp_min' ], limits[ 'temp_max' ], limits[ 'ntemp' ] )
        self.energy         = np.linspace( limits[ 'energy_min' ], limits[ 'energy_max' ], limits[ 'nenergy' ] )
        self.alpha          = np.linspace( limits[ 'Alpha_min' ], limits[ 'Alpha_max' ], limits[ 'nAlpha' ] )
        self.k_polar        = np.linspace( limits[ 'k_polar_min' ], limits[ 'k_polar_max' ], limits[ 'nk_polar' ] )
        self.k_azimuthal    = np.linspace( limits[ 'k_azimuthal_min' ], limits[ 'k_azimuthal_max' ], limits[ 'nk_azimuthal' ] )
        
        self.span = ( self.limits[ 'nAlpha' ], \
                      self.limits[ 'nk_polar' ], \
                      self.limits[ 'nk_azimuthal' ], \
                      2, \
                      2 )

        if not os.path.exists( 'data/' ):
            os.makedirs( 'data/' )

    def getRun( self ):

        DOF = itertools.product( enumerate( self.alpha ), \
                                 enumerate( self.k_polar ), \
                                 enumerate( self.k_azimuthal ) )
        
        path = self.data_folder + self.run_time + '-G0-T%03dE%03d' % self.label
        with open( path, 'r' ) as f:
            content = json.loads( f.read(), cls=NumericDecoder )
        g0_data = content[ 'data' ][ 'g_RET' ]

        run = list()
        
        for ( iAlpha, Alpha ), ( iXi, Xi ), ( iTheta, Theta ) in DOF: 
            index = ( self.label[0], self.label[1], iAlpha, iXi, iTheta )
            
            iTheta_F = iTheta + 1
            iTheta_B = iTheta - 1
            if iTheta + 1 > self.limits[ 'nk_azimuthal' ] - 1:
                iTheta_F = 0
            if iTheta - 1 < 0:
                iTheta_B = self.limits[ 'nk_azimuthal' ] - 1

            dg0 = ( g0_data[ 0, iXi, iTheta_F, :, : ] - g0_data[ 0, iXi, iTheta_B, :, : ] ) / 2.0 * self.limits[ 'dk_azimuthal' ]
            run.append( RunContainer( index, self.temp[ self.label[0] ], self.energy[ self.label[1] ], Alpha, Xi, Theta, self.constants, dg0  ) )
        
        return run 
    
    def updateData( self, array, func_str ):
        
        for element in array:
            index = element[ 'index' ][ 2 : len( element[ 'index' ] ) ]
            self.data[ func_str ][ index ] = element[ 'value' ]

    def initialiseData( self, label ):
        
        self.label = label
        self.data = np.zeros( shape=self.span, dtype=np.complex64 )

    def writeData( self, path ):
        
        path_complete = path + '-GR-T%03dE%03d' % ( self.label[0], self.label[1] )
        with open( path_complete, 'w' ) as f:
            f.write( json.dumps( { 'param' : self.limits.store, 'data': self.data }, cls=NumericEncoder, indent=4, sort_keys=True ) )
        f.close()

    def readData( self, path ):
        
        with open( path, 'r' ) as f:
            content = json.loads( f.read(), cls=NumericDecoder )
        self.data = content[ 'data' ]
        self.label = ( int( path[ -5 : -3 ] ), int( path[ -2 : ] ) )




