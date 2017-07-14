import numpy as np

class Limits:
    
    def __init__( self ):
        
        self.store = dict()

        self.store[ 'nenergy' ] =           10
        self.store[ 'nk_polar' ] =          2
        self.store[ 'nk_azimuthal' ] =      4
        self.store[ 'ntemp' ] =             10
        self.store[ 'nAlpha' ] =            2

        self.store[ 'energy_min' ] = -6.0
        self.store[ 'energy_max' ] = -self.store[ 'energy_min' ]

        self.store[ 'k_polar_min' ] = 0.0
        self.store[ 'k_polar_max' ] = np.pi

        self.store[ 'k_azimuthal_min' ] = 0.0
        self.store[ 'k_azimuthal_max' ] = 2.0 * np.pi

        self.store[ 'T_c' ] = 1.0
        self.store[ 'temp_min' ] = 0.1 * self.store[ 'T_c' ]
        self.store[ 'temp_max' ] = 0.1 * self.store[ 'T_c' ]

        self.store[ 'temp_increment' ] = 1.0 / 200.0 

        self.store[ 'Alpha_min' ] = -2.0 * 6
        self.store[ 'Alpha_max' ] = 0.0

        self.store[ 'a1' ] = 1.0
        self.store[ 'a2' ] = 1.0
        self.store[ 'a3' ] = 1.0
        self.store[ 'a4' ] = 1.0

        self.store[ 'B_z' ] = 1.0

        self.store[ 'gamma' ] = self.store[ 'a1' ] - self.store[ 'a4' ]
        self.store[ 'gamma_b' ] = self.store[ 'a2' ] + self.store[ 'a3' ]

        self.store[ 'denergy' ] = ( self.store[ 'energy_max' ] - self.store[ 'energy_min' ] ) / self.store[ 'nenergy' ]
        self.store[ 'dk_polar' ] = ( self.store[ 'k_polar_max' ] - self.store[ 'k_polar_min' ] ) / self.store[ 'nk_polar' ]
        self.store[ 'dk_azimuthal' ] = ( self.store[ 'k_azimuthal_max' ] - self.store[ 'k_azimuthal_min' ] ) / self.store[ 'nk_azimuthal' ]
        self.store[ 'dtemp' ] = ( self.store[ 'temp_max' ] - self.store[ 'temp_min' ] ) / self.store[ 'ntemp' ]
        self.store[ 'dAlpha' ] = ( self.store[ 'Alpha_max' ] - self.store[ 'Alpha_min' ] ) / self.store[ 'nAlpha' ]

        self.store[ 'info' ] = "The solution to the quasiclassical Eilenberger equation for a Weyl SC in uniform Magnetic field and parallel heat current"


    def __getitem__( self, key ):

        return self.store[ key ]

    def getConstants( self ):
        
        keys = [ 'T_c', 'nAlpha', 'dAlpha', 'temp_increment', 'gamma', 'gamma_b', 'temp_increment', 'B_z' ]

        return dict( ( key, self.store[ key ] ) for key in keys ) 

    def replaceStore( self, store ):

        self.store = store
