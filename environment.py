import numpy as np

class Environment:

    def __init__( self, value_set ):

        self.value_set = value_set
        self.store = dict()
        self.store[ 'DELTA_R_F' ] = self.DELTA_R_F
        self.store[ 'DELTA_R_B' ] = self.DELTA_R_B
        self.store[ 'DELTA_A_F' ] = self.DELTA_A_F
        self.store[ 'DELTA_A_B' ] = self.DELTA_A_B
        self.store[ 'SIGMA_R_F' ] = self.SIGMA_R_F
        self.store[ 'SIGMA_R_B' ] = self.SIGMA_R_B
        self.store[ 'SIGMA_A_F' ] = self.SIGMA_A_F
        self.store[ 'SIGMA_A_B' ] = self.SIGMA_A_B
        self.store[ 'SIGMA_K_F' ] = self.SIGMA_K_F
        self.store[ 'SIGMA_K_B' ] = self.SIGMA_K_B

    def __getitem__( self, key ):

        return self.store[ key ]()

    def DELTA_R_F( self ):
        
        VAL = self.value_set
        DV = VAL[ 'constants' ][ 'd_vector' ]

        a = 1.764 / ( 2 * np.pi ) 
        b = np.tanh( np.sqrt( VAL[ 'constants' ][ 'T_c' ] / VAL[ 'temperature' ] - 1.0 ) ) 
        c = np.tanh( VAL[ 'R_now' ] ) * np.exp( 1j * VAL[ 'P_now' ] )
        d = np.sin( VAL[ 'k_polar' ] ) * ( ( DV[ 'a1' ] - DV[ 'a4' ] ) * np.cos( VAL[ 'k_azimuthal' ] ) + 1j * ( DV[ 'a2' ] + DV[ 'a3' ] ) * np.sin( VAL[ 'k_azimuthal' ] ) ) 
        e = np.exp( 1j * VAL[ 'R_now' ] * np.cos( VAL[ 'P_now' ] ) * VAL[ 'constants' ][ 'supercurrent_phase' ] )
        
        if np.abs( a * b * c * d * e ) > 1.0:
            raise RuntimeWarning( 'The magnitude of the gap is greater than 1' )
        
        return a * b * c * d * e

    def DELTA_R_B( self ):

        return -np.conj( self.DELTA_R_F() )

    def DELTA_A_F( self ):
        
        VAL = self.value_set
        DV = VAL[ 'constants' ][ 'd_vector' ]

        a = 1.764 / ( 2 * np.pi ) 
        b = np.tanh( np.sqrt( VAL[ 'constants' ][ 'T_c' ] / VAL[ 'temperature' ] - 1.0 ) ) 
        c = np.tanh( VAL[ 'R_now' ] ) * np.exp( 1j * VAL[ 'P_now' ] )
        d = np.sin( VAL[ 'k_polar' ] ) * ( ( DV[ 'a1' ] - DV[ 'a4' ] ) * np.cos( VAL[ 'k_azimuthal' ] ) + 1j * ( DV[ 'a2' ] + DV[ 'a3' ] ) * np.sin( VAL[ 'k_azimuthal' ] ) ) 
        e = np.exp( 1j * VAL[ 'R_now' ] * np.cos( VAL[ 'P_now' ] ) * VAL[ 'constants' ][ 'supercurrent_phase' ] )
        
        if np.abs( a * b * c * d * e ) > 1.0:
            raise RuntimeWarning( 'The magnitude of the gap is greater than 1' )
        
        return a * b * c * d * e

    def DELTA_A_B( self ):

        return -np.conj( self.DELTA_A_F() )

    def SIGMA_R_F( self ):

        return -1j * 0.01
    
    def SIGMA_R_B( self ):

        return 1j * 0.01
    
    def SIGMA_A_F( self ):

        return 1j * 0.01
    
    def SIGMA_A_B( self ):

        return -1j * 0.01

    def SIGMA_K_F( self ):

        return 1j * 0.01

    def SIGMA_K_B( self ):

        return -1j * 0.01
