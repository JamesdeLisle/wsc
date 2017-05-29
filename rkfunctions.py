import numpy as np
import environment as env

class RKFunctions:

    def __init__( self, value_set, func_val ):
        
        self.func_val = func_val
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
        
        return 1j * ( 2 * VAL[ 'energy' ] * self.func_val \
                - ENV[ 'SIGMA_R_F' ] * self.func_val \
                + ENV[ 'SIGMA_R_B' ] * self.func_val \
                + np.conj( ENV[ 'DELTA_R_F' ] ) * self.func_val * self.func_val \
                + ENV[ 'DELTA_R_F' ] )
    
    def GAM_R_B( self ):
        
        VAL = self.value_set
        ENV = self.environment

        return 1j * ( -2 * VAL[ 'energy' ] * self.func_val \
                - ENV[ 'SIGMA_R_B' ] * self.func_val \
                + ENV[ 'SIGMA_R_F' ] * self.func_val \
                + ENV[ 'DELTA_R_F' ] * self.func_val * self.func_val \
                - ENV[ 'DELTA_R_B' ] )

    def DIST_F( self ):

        VAL = self.value_set
        ENV = self.environment
        AV = self.value_set[ 'data' ]
        
        return 1j * ( AV[ 'GAM_R_F' ] * np. conj( ENV[ 'DELTA_R_F' ] ) * self.func_val \
                - ENV[ 'SIGMA_R_F' ] * self.func_val \
                + ENV[ 'DELTA_A_F' ] * AV[ 'GAM_A_B' ] * self.func_val \
                + ENV[ 'SIGMA_A_F' ] * self.func_val \
                + AV[ 'GAM_R_F' ] * ENV[ 'SIGMA_K_B' ] * AV[ 'GAM_A_B' ] \
                + ENV[ 'SIGMA_K_F' ] )

    def DIST_B( self ):

        VAL = self.value_set
        ENV = self.environment
        AV = self.value_set[ 'data' ]

        return 1j * ( AV[ 'GAM_R_B' ] * ENV[ 'DELTA_R_F' ] * self.func_val \
                - ENV[ 'SIGMA_R_B' ] * self.func_val \
                + np.conj( ENV[ 'DELTA_A_F' ] ) * AV[ 'GAM_A_F' ] * self.func_val \
                + ENV[ 'SIGMA_A_B' ] * self.func_val \
                + AV[ 'GAM_R_B' ] * ENV[ 'SIGMA_K_F' ] * AV[ 'GAM_A_F' ] \
                + ENV[ 'SIGMA_K_B' ] )

