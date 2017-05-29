import itertools
import numpy as np

class LDOS:

    def __init__( self, param_space ):

        self.param_space = param_space
        self.limits = self.param_space.limits
        self.data = param_space.data
        self.LDOS = np.zeros( shape=( self.limits[ 'ntemp' ], \
                                      self.limits[ 'nenergy' ], \
                                      self.limits[ 'nspace_radial' ], \
                                      self.limits[ 'nspace_azimuthal' ] ) )

    def compute( self ):

        dtheta = self.limits[ 'dk_azimuthal' ]
        dxi = self.limits[ 'dk_polar' ]
        DOF = itertools.product( enumerate( self.param_space.temp ), \
                                 enumerate( self.param_space.energy ), \
                                 enumerate( self.param_space.space_radial ), \
                                 enumerate( self.param_space.space_azimuthal ) )
         
        for ( iT, T ), ( iE, E ), ( iR, R ), ( iphi, phi ) in DOF:
            index_out = ( iT, iE, iR, iphi )
            for ixi, xi in enumerate( self.param_space.k_polar ):
                dosXi = 0.0
                for itheta, theta in enumerate( self.param_space.k_azimuthal ):
                    dosTh = 0.0
                    index_in = ( iT, iE, iR, iphi, ixi, itheta )
                    dosTh = 1j * 1.0 / ( 4.0 * np.pi )
                    dosTh = dosTh * ( 1 - self.data[ 'GAM_R_F' ][ index_in ] * self.data[ 'GAM_R_B' ][ index_in ] )
                    dosTh = dosTh / ( 1 + self.data[ 'GAM_R_F' ][ index_in ] * self.data[ 'GAM_R_B' ][ index_in ] )
                    dosTh = dosTh * dtheta / 3.0
                    if itheta == 0 or itheta == self.limits[ 'nk_azimuthal' ]:
                        pass
                    elif itheta % 2 == 0:
                        dosTh = dosTh * 4.0
                    else:
                        dosTh = dosTh * 2.0
                    dosXi = dosXi + np.imag ( dosTh )
                dosXi = dosXi * np.sin( xi ) * dxi / 3.0
                if ixi == 0 or ixi == self.limits[ 'nk_polar' ]:
                    pass
                elif ixi % 2 == 0:
                    dosXi = dosXi * 4.0
                else:
                    dosXi = dosXi * 2.0
                self.LDOS[ index_out ] += dosXi
            
    
    def writeData( self, path ):
        
        DOF = itertools.product( enumerate( self.param_space.temp ), \
                                 enumerate( self.param_space.energy ), \
                                 enumerate( self.param_space.space_radial ), \
                                 enumerate( self.param_space.space_azimuthal ) )
        
        with open( path, 'w' ) as f:
            for ( iT, T ), ( iE, E ), ( iR, R ), ( iphi, phi ) in DOF:
                f.write( '%f %f %f %f %f\n' % ( T, E, R, phi, self.LDOS[ iT, iE, iR, iphi ] ) )
        f.close()

