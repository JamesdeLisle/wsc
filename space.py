import itertools
import container as cont
import numpy as np
from jsci.Coding import NumericEncoder, NumericDecoder
import json

class ParamSpace:

    def __init__( self, limits ):
        
        """defines the parameter space"""
        self.limits = limits
        self.constants = self.limits.getConstants()
        
        self.strings = [ 'GAM_R_F', 'GAM_R_B', 'GAM_A_F', 'GAM_A_B', 'DIST_F', 'DIST_B' ]

        self.energy         = np.linspace( limits[ 'energy_min' ], limits[ 'energy_max' ], limits[ 'nenergy' ] )
        self.space_radial   = np.linspace( 0, limits[ 'space_radial_max' ], limits[ 'nspace_radial' ] )
        self.space_azimuthal= np.linspace( limits[ 'space_azimuthal_min' ], limits[ 'space_azimuthal_max' ], limits[ 'nspace_azimuthal' ] )
        self.k_polar        = np.linspace( limits[ 'k_polar_min' ], limits[ 'k_polar_max' ], limits[ 'nk_polar' ] )
        self.k_azimuthal    = np.linspace( limits[ 'k_azimuthal_min' ], limits[ 'k_azimuthal_max' ], limits[ 'nk_azimuthal' ] )
        self.temp           = np.linspace( limits[ 'temp_min' ], limits[ 'temp_max' ], limits[ 'ntemp' ] )
        
        self.data = span = ( self.limits[ 'ntemp' ], \
                             self.limits[ 'nenergy' ], \
                             self.limits[ 'nspace_radial' ], \
                             self.limits[ 'nspace_azimuthal' ], \
                             self.limits[ 'nk_polar' ], \
                             self.limits[ 'nk_azimuthal' ] )
        
        self.data = { string : np.zeros( shape=span, dtype=np.complex64 ) for string in self.strings } 

    def getSlice( self, iT, iE, iXi, iTheta ):

        out = dict()
        out[ 'GAM_R_F' ] = self.data[ 'GAM_R_F' ][ iT, iE, :, :, iXi, iTheta ]
        out[ 'GAM_R_B' ] = self.data[ 'GAM_R_B' ][ iT, iE, :, :, iXi, iTheta ]
        
        return out

    def getRun( self, func_str ):

        DOF = itertools.product( enumerate( self.temp ), \
                                 enumerate( self.energy ), \
                                 enumerate( self.space_radial ), \
                                 enumerate( self.space_azimuthal ), \
                                 enumerate( self.k_polar ), \
                                 enumerate( self.k_azimuthal ) )
        
        run = list()

        for ( iT, T ), ( iE, E ), ( iR, R ), ( iPhi, Phi ), ( iXi, Xi ), ( iTheta, Theta ) in DOF: 
            index = ( iT, iE, iR, iPhi, iXi, iTheta )
            run.append( cont.RunContainer( func_str, index, T, E, R, Phi, Xi, Theta, self.constants, self.getSlice( iT, iE, iXi, iTheta ) ) )
        
        return run 
    
    def updateData( self, array, func_str ):

        for element in array:

            self.data[ func_str ][ element[ 'index' ] ] = element[ 'value' ]

    def writeData( self, path ):
        
        with open( path, 'w' ) as f:
            f.write( json.dumps( { 'param' : self.limits.store, 'data': self.data }, cls=NumericEncoder, indent=4, sort_keys=True ) )
        f.close()

    def readData( self, path ):
        
        with open( path, 'r' ) as f:
            content = json.loads( f.read(), cls=NumericDecoder )
        self.data = content[ 'data' ]
