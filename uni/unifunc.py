import gen.env as env 
import numpy as np

class Uniform:

    def __init__( self, value_set ):

        self.value_set = value_set
        self.environment = env.Environment( value_set )
        self.store = dict()
        self.store[ 'GAM_R_F' ] = self.GAM_R_F
        self.store[ 'GAM_R_B' ] = self.GAM_R_B
        self.store[ 'GAM_A_F' ] = self.GAM_A_F
        self.store[ 'GAM_A_B' ] = self.GAM_A_B
        self.store[ 'DIST_F' ] = self.DIST_F
        self.store[ 'DIST_B' ] = self.DIST_B
        self.store[ 'g_RET' ] = self.g_RET
        self.store[ 'g_KEL' ] = self.g_KEL

    def __getitem__( self, key ):

        return self.store[ key ]()
    
    def GAM_R_F( self ):
        
        ENV = self.environment
        VAL = self.value_set

        epsilon = VAL[ 'energy' ] - ( ENV[ 'SIGMA_R_F' ] - ENV[ 'SIGMA_R_B' ] ) / 2.0

        return ENV[ 'DELTA_R_F' ] / ( epsilon + 1j * np.sqrt( ENV[ 'DELTA_R_F' ] * np.conj( ENV[ 'DELTA_R_F' ] ) - epsilon * epsilon ) )

    def GAM_R_B( self ):
        
        ENV = self.environment
        VAL = self.value_set

        epsilon = VAL[ 'energy' ] - ( ENV[ 'SIGMA_R_F' ] - ENV[ 'SIGMA_R_B' ] ) / 2.0

        return -np.conj( ENV[ 'DELTA_R_B' ] ) / ( epsilon + 1j * np.sqrt( ENV[ 'DELTA_R_B' ] * np.conj( ENV[ 'DELTA_R_B' ] ) - epsilon * epsilon ) )
    
    def GAM_A_F( self ):
        
        ENV = self.environment
        VAL = self.value_set

        epsilon = VAL[ 'energy' ] - ( ENV[ 'SIGMA_R_F' ] - ENV[ 'SIGMA_R_B' ] ) / 2.0

        return ENV[ 'DELTA_A_F' ] / ( epsilon + 1j * np.sqrt( ENV[ 'DELTA_A_F' ] * np.conj( ENV[ 'DELTA_A_F' ] ) - epsilon * epsilon ) )

    def GAM_A_B( self ):
        
        ENV = self.environment
        VAL = self.value_set

        epsilon = VAL[ 'energy' ] - ( ENV[ 'SIGMA_R_F' ] - ENV[ 'SIGMA_R_B' ] ) / 2.0

        return -np.conj( ENV[ 'DELTA_A_B' ] ) / ( epsilon + 1j * np.sqrt( ENV[ 'DELTA_A_B' ] * np.conj( ENV[ 'DELTA_A_B' ] ) - epsilon * epsilon ) )

    def DIST_F( self ):
        
        VAL = self.value_set
        ENV = self.environment 
        
        return ( 1.0 -self.GAM_R_F() * self.GAM_A_B() ) \
                * ( -VAL[ 'energy' ] ) \
                / ( 2.0 * VAL[ 'temperature' ] * VAL[ 'temperature' ] \
                * np.cosh( VAL[ 'energy' ] / ( 2.0 * VAL[ 'temperature' ] ) ) \
                * np.cosh( VAL[ 'energy' ] / ( 2.0 * VAL[ 'temperature' ] ) ) ) \
                * VAL[ 'Z_now' ] * VAL[ 'constants' ][ 'temp_increment' ] 
    
    def DIST_B( self ):
        
        VAL = self.value_set
        ENV = self.environment 
        
        return ( 1.0 - self.GAM_R_F() * self.GAM_A_B() ) \
                * ( 2.0 * np.pi * VAL[ 'energy' ] ) \
                / ( 2.0 * VAL[ 'temperature' ] * VAL[ 'temperature' ] \
                * np.cosh( -2.0 * np.pi * VAL[ 'energy' ] / ( 2.0 * VAL[ 'temperature' ] ) ) \
                * np.cosh( -2.0 * np.pi * VAL[ 'energy' ] / ( 2.0 * VAL[ 'temperature' ] ) ) ) \
                * VAL[ 'Z_now' ] * VAL[ 'constants' ][ 'temp_increment' ] 

    def g_RET( self ):
        
        NORM = np.zeros( shape=(2,2), dtype=np.complex128 )
        NORM[ 0, 0 ] = 1.0 - self.GAM_R_F() * self.GAM_R_B() 
        NORM[ 1, 1 ] = 1.0 - self.GAM_R_F() * self.GAM_R_B() 

        GRET = np.zeros( shape=(2,2), dtype=np.complex128 )
        GRET[ 0, 0 ] = 1 + self.GAM_R_F() * self.GAM_R_B()
        GRET[ 1, 1 ] = -1 - self.GAM_R_F() * self.GAM_R_B()
        GRET[ 0, 1 ] = 2 * self.GAM_R_F()
        GRET[ 1, 0 ] = -2 * self.GAM_R_B()

        return -1j * np.pi * np.dot( NORM, GRET )

    def g_KEL( self ):
        
        NORMR = np.zeros( shape=(2,2), dtype=np.complex128 )
        NORMR[ 0, 0 ] = 1.0 - self.GAM_R_F() * self.GAM_R_B() 
        NORMR[ 1, 1 ] = 1.0 - self.GAM_R_F() * self.GAM_R_B() 
        NORMA = np.zeros( shape=(2,2), dtype=np.complex128 )
        NORMA[ 0, 0 ] = 1.0 - self.GAM_A_F() * self.GAM_A_B() 
        NORMA[ 1, 1 ] = 1.0 - self.GAM_A_F() * self.GAM_A_B() 

        GKEL = np.zeros( shape=(2,2), dtype=np.complex128 )
        GKEL[ 0, 0 ] = self.DIST_F() - self.GAM_R_F() * self.DIST_B() * self.GAM_A_B() 
        GKEL[ 1, 1 ] = self.DIST_B() - self.GAM_R_B() * self.DIST_F() * self.GAM_A_F() 
        GKEL[ 0, 1 ] = -self.GAM_R_F() * self.DIST_B() + self.DIST_F() * self.GAM_A_F() 
        GKEL[ 1, 0 ] = -self.GAM_R_B() * self.DIST_F() + self.DIST_B() * self.GAM_A_B() 

        return -2j * np.pi * np.dot( np.dot( NORMR, GKEL ), NORMA )
