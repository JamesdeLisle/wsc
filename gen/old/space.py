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
        
        self.span = ( self.limits[ 'nspace_radial' ], \
                      self.limits[ 'nspace_azimuthal' ], \
                      self.limits[ 'nk_polar' ], \
                      self.limits[ 'nk_azimuthal' ] )
        
    def getSlice( self, iXi, iTheta ):

        out = dict()
        out[ 'GAM_R_F' ] = self.data[ 'GAM_R_F' ][ :, :, iXi, iTheta ]
        out[ 'GAM_R_B' ] = self.data[ 'GAM_R_B' ][ :, :, iXi, iTheta ]
        
        return out

    def getRun( self, iT, iE, func_str ):

        DOF = itertools.product( enumerate( self.space_radial ), \
                                 enumerate( self.space_azimuthal ), \
                                 enumerate( self.k_polar ), \
                                 enumerate( self.k_azimuthal ) )
        
        run = list()

        for ( iR, R ), ( iPhi, Phi ), ( iXi, Xi ), ( iTheta, Theta ) in DOF: 
            index = ( iT, iE, iR, iPhi, iXi, iTheta )
            run.append( cont.RunContainer( func_str, index, self.temp[ iT ], self.energy[ iE ], R, Phi, Xi, Theta, self.constants, self.getSlice( iXi, iTheta ) ) )
        
        return run 
    
    def updateData( self, array, func_str ):
        
        for element in array:
            index = element[ 'index' ][ 2 : len( element[ 'index' ] ) ]
            self.data[ func_str ][ index ] = element[ 'value' ]

    def initialiseData( self, label ):
        
        self.label = label
        self.data = { string : np.zeros( shape=self.span, dtype=np.complex64 ) for string in self.strings }

    def writeData( self, path ):
        
        path_complete = path + '-T%02dE%02d' % ( self.label[0], self.label[1] )
        with open( path_complete, 'w' ) as f:
            f.write( json.dumps( { 'param' : self.limits.store, 'data': self.data }, cls=NumericEncoder, indent=4, sort_keys=True ) )
        f.close()

    def readData( self, path ):
        
        with open( path, 'r' ) as f:
            content = json.loads( f.read(), cls=NumericDecoder )
        self.data = content[ 'data' ]
        self.label = ( int( path[ -5 : -3 ] ), int( path[ -2 : ] ) )
