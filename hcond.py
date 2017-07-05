import itertools
import numpy as np

class HCond: 

    def __init__( self, param_space ):

        self.param_space = param_space
        self.limits = self.param_space.limits
        self.data = self.param_space.data
        self.J_z = np.zeros( shape=(  self.limits[ 'nspace_radial' ], \
                                      self.limits[ 'nspace_azimuthal' ] ) )

    def compute( self ):
        
        dTheta = self.limits[ 'dk_azimuthal' ]
        dXi = self.limits[ 'dk_polar' ]
        dE = self.limits[ 'denergy' ]

        for iR, R in self.param_space.space_radial:
            for iPhi, Phi in self.param_space.space_azimuthal:
                heatE = 0.0
                for iE, E in self.param_space.energy:
                    heatG = 0.0
                    for iXi, Xi in self.param_space.k_polar:
                        for iTheta, Theta in self.param_space.k_azimuthal:
                            index = ( 0, iE, iR, iPhi, iXi, iTheta )
                            GAM_A_F = -np.conj( self.data[ 'GAM_R_B' ][ index ] )
                            GAM_A_B = -np.conj( self.data[ 'GAM_R_F' ][ index ] )
                            heat = self.data[ 'DIST_F' ][ index ] * ( 1.0 + self.data[ 'GAM_R_B' ][ index ] * GAM_A_F ) 
                            heat += self.data[ 'DIST_B' ][ index ] * ( 1.0 + self.data[ 'GAM_R_F' ][ index ] * GAM_A_B )
                            heat /= ( 4.0 * ( 1.0 + self.data[ 'GAM_R_F' ][ index ] * self.data[ 'GAM_R_B' ][ index ] ) * ( 1.0 + GAM_A_F * GAM_A_B ) )
                            heat /= heat / ( 4.0 * np.pi )
                            heat *= -2.0
                            heat *= dTheta / 3.0 

                            if iTheta == 0 or iTheta == self.limits[ 'nk_azimuthal' ] - 1:
                                pass
                            elif iTheta % 2 == 0:
                                heat *= 4.0
                            else:
                                heat *= 2.0
                            heatG += np.real( heat )

                        heatG *= np.sin( Xi ) * np.cos( Xi ) * dXi / 3.0
                        if iXi == 0 or iXi == self.limits[ 'nk_polar' ] - 1:
                            pass
                        elif iXi % 2 == 0:
                            heatG *= 4.0
                        else:
                            heatG *= 2.0
                        heatE += heatG 
                    
                    heatE *= E *dE / 3.0
                    if iE == 0 or iE == self.limits[ 'nenergy' ] - 1:
                        pass
                    elif iE % 2 == 0:
                        heatE *= 4.0
                    else:
                        heatE *= 2.0
                    self.J_z[ iR, iPhi ] += heatE
    
    def writeData( self, path ):
        
        DOF = itertools.product( enumerate( self.param_space.temp ), \
                                 enumerate( self.param_space.energy ), \
                                 enumerate( self.param_space.space_radial ), \
                                 enumerate( self.param_space.space_azimuthal ) )
        
        with open( path, 'w' ) as f:
            for ( iT, T ), ( iE, E ), ( iR, R ), ( iphi, phi ) in DOF:
                f.write( '%f %f %f %f %f\n' % ( T, E, R, phi, self.J_z[ iT, iE, iR, iphi ] ) )
        f.close()

                    
