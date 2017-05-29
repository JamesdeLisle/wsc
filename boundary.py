import numpy as np
import environment as env


class Boundary:

    def __init__( self, value_set ):
        
        self.value_set = value_set
        self.environment = env.Environment( value_set )
        self.store = dict()
        self.store[ 'GAM_R_F' ] = self.GAM_R_F
        self.store[ 'GAM_R_B' ] = self.GAM_R_B
        self.store[ 'DIST_F' ] = self.DIST_F
        self.store[ 'DIST_B' ] = self.DIST_B

    def get( self ):

        return self.store[ self.value_set[ 'func_str' ] ]()

    def GAM_R_F( self ):

        VAL = self.value_set
        ENV = self.environment

        epsilon = VAL[ 'energy' ] - ( ENV[ 'SIGMA_R_F' ] - ENV[ 'SIGMA_R_B' ] ) / 2.0

        return -ENV[ 'DELTA_R_F' ] / ( epsilon + 1j * np.sqrt( ENV[ 'DELTA_R_F' ] * np.conj( ENV[ 'DELTA_R_F' ] ) - epsilon * epsilon ) )
    
    def GAM_R_B( self ):

        VAL = self.value_set
        ENV = self.environment

        epsilon = VAL[ 'energy' ] - ( ENV[ 'SIGMA_R_F' ] - ENV[ 'SIGMA_R_B' ] ) / 2.0

        return -ENV[ 'DELTA_R_B' ] / ( epsilon + 1j * np.sqrt( ENV[ 'DELTA_R_F' ] * np.conj( ENV[ 'DELTA_R_F' ] ) - epsilon * epsilon ) )

    def DIST_F( self ):
        
        VAL = self.value_set
        ENV = self.environment 
        
        return VAL[ 'temp_gradient' ] \
                * ( 1.0 - VAL[ 'data' ][ 'GAM_R_F' ] * VAL[ 'data' ][ 'GAM_A_B' ] ) \
                * ( -2.0 * np.pi * VAL[ 'energy' ] ) \
                / ( 2.0 * VAL[ 'temperature' ] * VAL[ 'temperature' ] \
                * np.cosh( 2.0 * np.pi * VAL[ 'energy' ] / ( 2.0 * VAL[ 'temperature' ] ) ) \
                * np.cosh( 2.0 * np.pi * VAL[ 'energy' ] / ( 2.0 * VAL[ 'temperature' ] ) ) )
    
    def DIST_B( self ):
        
        VAL = self.value_set
        ENV = self.environment 
        
        return VAL[ 'temp_gradient' ] \
                * ( 1.0 - VAL[ 'data' ][ 'GAM_R_F' ] * VAL[ 'data' ][ 'GAM_A_B' ] ) \
                * ( 2.0 * np.pi * VAL[ 'energy' ] ) \
                / ( 2.0 * VAL[ 'temperature' ] * VAL[ 'temperature' ] \
                * np.cosh( -2.0 * np.pi * VAL[ 'energy' ] / ( 2.0 * VAL[ 'temperature' ] ) ) \
                * np.cosh( -2.0 * np.pi * VAL[ 'energy' ] / ( 2.0 * VAL[ 'temperature' ] ) ) )
