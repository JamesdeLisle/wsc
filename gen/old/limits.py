import numpy as np
import container as cont

class Limits:
    
    def __init__( self ):
        
        self.store = dict()

        self.store[ 'nenergy' ] =           10
        self.store[ 'nspace_radial' ] =     2
        self.store[ 'nspace_azimuthal' ] =  2
        self.store[ 'nk_polar' ] =          2
        self.store[ 'nk_azimuthal' ] =      2
        self.store[ 'ntemp' ] =             10
        self.store[ 'nAlpha' ] =            2

        self.store[ 'energy_min' ] = -6.0
        self.store[ 'energy_max' ] = -self.store[ 'energy_min' ]

        self.store[ 'space_radial_max' ] = 5.0

        self.store[ 'space_azimuthal_min' ] = 0.0
        self.store[ 'space_azimuthal_max' ] = 2.0 * np.pi

        self.store[ 'k_polar_min' ] = 0.0
        self.store[ 'k_polar_max' ] = np.pi

        self.store[ 'k_azimuthal_min' ] = 0.0
        self.store[ 'k_azimuthal_max' ] = 2.0 * np.pi

        self.store[ 'T_c' ] = 1.0
        self.store[ 'temp_min' ] = 0.1 * self.store[ 'T_c' ]
        self.store[ 'temp_max' ] = 0.1 * self.store[ 'T_c' ]

        self.store[ 'temp_increment' ] = 1.0 / 200.0 

        self.store[ 'Alpha_limit' ] = -2.0 * self.store[ 'space_radial_max' ]

        self.store[ 'denergy' ] = ( self.store[ 'energy_max' ] - self.store[ 'energy_min' ] ) / self.store[ 'nenergy' ]
        self.store[ 'dspace_radial' ] = self.store[ 'space_radial_max' ] / self.store[ 'nspace_radial' ]
        self.store[ 'dspace_azimuthal' ] = ( self.store[ 'space_azimuthal_max' ] - self.store[ 'space_azimuthal_min' ] ) / self.store[ 'nspace_azimuthal' ]
        self.store[ 'dk_polar' ] = ( self.store[ 'k_polar_max' ] - self.store[ 'k_polar_min' ] ) / self.store[ 'nk_polar' ]
        self.store[ 'dk_azimuthal' ] = ( self.store[ 'k_azimuthal_max' ] - self.store[ 'k_azimuthal_min' ] ) / self.store[ 'nk_azimuthal' ]
        self.store[ 'dtemp' ] = ( self.store[ 'temp_max' ] - self.store[ 'temp_min' ] ) / self.store[ 'ntemp' ]
        self.store[ 'dAlpha' ] = self.store[ 'Alpha_limit' ] / self.store[ 'nAlpha' ]

        self.store[ 'info' ] = "The solution to the quasiclassical Eilenberger equation for a Weyl SC with vortex and lateral supercurrent"


    def __getitem__( self, key ):

        return self.store[ key ]

    def getConstants( self ):

        return cont.Constants( self.store[ 'T_c' ], \
                               self.store[ 'Alpha_limit' ], \
                               self.store[ 'nAlpha' ], \
                               self.store[ 'dAlpha' ], \
                               self.store[ 'nspace_radial' ], \
                               self.store[ 'nspace_azimuthal' ], \
                               self.store[ 'dspace_radial' ], \
                               self.store[ 'dspace_azimuthal' ], \
                               self.store[ 'space_radial_max' ], \
                               self.store[ 'space_azimuthal_min' ], \
                               self.store[ 'space_azimuthal_max' ], \
                               self.store[ 'temp_increment' ] )   

    def replaceStore( self, store ):

        self.store = store
