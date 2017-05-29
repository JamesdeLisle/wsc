import numpy as np
import itertools

class Normalisation:

    def __init__( self, param_space ):

        self.param_space = param_space
        self.limits = self.param_space.limits
        self.data = param_space.data
        self.NORM = np.zeros( shape=( self.limits[ 'ntemp' ], \
                                      self.limits[ 'nenergy' ], \
                                      self.limits[ 'nspace_radial' ], \
                                      self.limits[ 'nspace_azimuthal' ], \
                                      self.limits[ 'nk_polar' ],\
                                      self.limits[ 'nk_azimuthal' ]) )
    def compute( self ):

        
        DOF = itertools.product( enumerate( self.param_space.temp ), \
                                 enumerate( self.param_space.energy ), \
                                 enumerate( self.param_space.space_radial ), \
                                 enumerate( self.param_space.space_azimuthal ), \
                                 enumerate( self.param_space.k_polar ), \
                                 enumerate( self.param_space.k_azimuthal ) )

        for ( iT, T ), ( iE, E ), ( iR, R ), ( iphi, phi ), ( ixi, xi ), ( itheta, theta ) in DOF:

            index_in = ( iT, iE, iR, iphi, ixi, itheta )
            a = -1j * np.pi / ( 1 - self.data[ 'GAM_R_F' ][ index_in ] * self.data[ 'GAM_R_B' ][ index_in ] )
            b = a
            alpha = 1 + self.data[ 'GAM_R_F' ][ index_in ] * self.data[ 'GAM_R_B' ][ index_in ]
            beta = 2 * self.data[ 'GAM_R_F' ][ index_in ]
            gamma = -2 * self.data[ 'GAM_R_B' ][ index_in ]
            delta = -1 - self.data[ 'GAM_R_F' ][ index_in ] * self.data[ 'GAM_R_B' ][ index_in ]
            a_00 = a * alpha * a * alpha + a * alpha * b * gamma
            a_01 = b * gamma * a * beta + b * gamma * b * gamma
            a_10 = a * alpha * a * beta + a * beta * b * delta
            a_11 = b * gamma * a * beta + b * delta * b * delta
            
            print a_00
            print a_01
            print a_10 
            print a_11
            print a
            print alpha
            print beta
            print gamma
            print delta
            print '\n'

