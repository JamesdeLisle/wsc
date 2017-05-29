import numpy as np
import itertools
from bisect import bisect_left

class RunContainer:

    def __init__( self, func_str, index, temperature, energy, space_radial, space_azimuthal, k_polar, k_azimuthal, constants, data  ):
        
        self.store = dict()
        self.store[ 'index' ] = index
        self.store[ 'func_str' ] = func_str
        self.store[ 'temperature' ] = temperature
        self.store[ 'energy' ] = energy
        self.store[ 'space_radial' ] = space_radial
        self.store[ 'space_azimuthal' ] = space_azimuthal
        self.store[ 'k_polar' ] = k_polar
        self.store[ 'k_azimuthal' ] = k_azimuthal 
        self.store[ 'constants' ] = constants
        self.store[ 'data'] = data 
        
        if func_str in [ 'GAM_R_B', 'DIST_B' ]:
            if self.store[ 'constants' ][ 'Alpha_limit' ] < 0:
                self.store[ 'constants' ][ 'Alpha_limit' ] = -self.store[ 'constants' ][ 'Alpha_limit' ]
            if self.store[ 'constants' ][ 'dAlpha' ] > 0:
                self.store[ 'constants' ][ 'dAlpha' ] = -self.store[ 'constants' ][ 'dAlpha' ]
        else:
            if self.store[ 'constants' ][ 'Alpha_limit' ] > 0:
                self.store[ 'constants' ][ 'Alpha_limit' ] = -self.store[ 'constants' ][ 'Alpha_limit' ]
            if self.store[ 'constants' ][ 'dAlpha' ] < 0:
                self.store[ 'constants' ][ 'dAlpha' ] = -self.store[ 'constants' ][ 'dAlpha' ]


    def __getitem__( self, key ):
        
        return self.store[ key ]
   
    def getSet( self, Alpha ):
        
        out =  ValueSet( self.store[ 'func_str' ], \
                         self.store[ 'temperature' ], \
                         self.store[ 'energy' ], \
                         self.store[ 'space_radial' ], \
                         self.store[ 'space_azimuthal' ], \
                         self.store[ 'k_polar' ],  \
                         self.store[ 'k_azimuthal' ], \
                         self.store[ 'constants' ], \
                         Alpha )
        
        R = out[ 'R_now' ]
        P = out[ 'P_now' ]
        
        if R > self.store[ 'constants' ][ 'space_radial_max' ]:
            R = self.store[ 'constants' ][ 'space_radial_max' ]
        
        strings = [ 'GAM_R_F', 'GAM_R_B' ]
            
        data = dict()
        for string in strings:
            data[ string ] = 0.0 
        
        R_lst = np.linspace( 0, self.store[ 'constants' ][ 'space_radial_max' ], self.store[ 'constants' ][ 'nspace_radial' ] )
        P_lst = np.linspace( 0, self.store[ 'constants' ][ 'space_azimuthal_max' ], self.store[ 'constants' ][ 'nspace_azimuthal' ] )
        
        pos_R = bisect_left( R_lst, R )
        pos_P = bisect_left( P_lst, P )
       
        if self.store[ 'func_str' ] == 'DIST_F':
            relevant_string = 'GAM_R_F'
        elif self.store[ 'func_str' ] == 'DIST_B':
            relevant_string = 'GAM_R_B'

        try:
            if self.store[ 'func_str' ] in [ 'DIST_F', 'DIST_B' ]: 
                counter = 0
                for ir in range( pos_R - 2, pos_R + 3, 1 ):
                    if ir - ( len( R_lst ) - 1 ) > 0:
                        ir = len( R_lst ) - 1
                    elif ir < 0:
                        ir = 0
                    if np.abs( R - R_lst[ ir ] ) < self.store[ 'constants' ][ 'dspace_radial' ]:
                        for ip in range( pos_P - 2, pos_P + 3, 1 ):
                            if ip - ( len( P_lst ) - 1 ) > 0:
                                ip = ip - len( P_lst )
                            elif ip < 0:
                                ip = len( P_lst ) + ip 
                            if np.abs( P - P_lst[ ip ] ) < self.store[ 'constants' ][ 'dspace_azimuthal' ]:
                                data[ relevant_string ] += self.store[ 'data' ][ relevant_string ][ ir, ip ]
                                counter += 1
        except IndexError:
            print ir, ip
            if counter != 0:
                data[ relevant_string ] = data[ relevant_string ] / counter
            
        #TODO might need fixing.
        data[ 'GAM_A_F' ] = -np.conj( data[ 'GAM_R_B' ] )
        data[ 'GAM_A_B' ] = -np.conj( data[ 'GAM_R_F' ] )

        out[ 'data' ] = data

        return out
                               
class Constants:

    def __init__( self, T_c, Alpha_limit, nAlpha, dAlpha, \
                                                  nspace_radial, \
                                                  nspace_azimuthal,  \
                                                  dspace_radial, \
                                                  dspace_azimuthal, \
                                                  space_radial_max, \
                                                  space_azimuthal_min, \
                                                  space_azimuthal_max, \
                                                  temp_increment ):

        self.store = dict()
        self.store[ 'T_c' ] = T_c
        self.store[ 'Alpha_limit' ] = Alpha_limit
        self.store[ 'nAlpha' ] = nAlpha
        self.store[ 'dAlpha' ] = dAlpha
        self.store[ 'dspace_radial' ] = dspace_radial
        self.store[ 'dspace_azimuthal' ] = dspace_azimuthal
        self.store[ 'nspace_radial' ] = nspace_radial
        self.store[ 'nspace_azimuthal' ] = nspace_azimuthal
        self.store[ 'space_radial_max' ] = space_radial_max 
        self.store[ 'space_azimuthal_min' ] = space_azimuthal_min
        self.store[ 'space_azimuthal_max' ] = space_azimuthal_max
        self.store[ 'temp_increment' ] = temp_increment

    
    def __getitem__( self, key ):
        
        return self.store[ key ]

    def __setitem__( self, key, value ):

        self.store[ key ] = value

    
class ValueSet:
    
    def __init__( self, func_str, temperature, energy, space_radial, space_azimuthal, k_polar, k_azimuthal, constants, Alpha ):
        
        self.store = dict()
        self.store[ 'func_str' ] = func_str
        self.store[ 'temperature' ] = temperature
        self.store[ 'energy' ] = energy
        self.store[ 'space_radial' ] = space_radial
        self.store[ 'space_azimuthal' ] = space_azimuthal
        self.store[ 'k_polar' ] = k_polar
        self.store[ 'k_azimuthal' ] = k_azimuthal 
        self.store[ 'constants' ] = constants
        self.store[ 'Alpha' ] = Alpha
        self.transform()
        if self.store[ 'func_str' ] in [ 'DIST_F', 'DIST_B' ]:
            self.getTempGradient()
        
    def __getitem__( self, key ):
        
        return self.store[ key ]

    def __setitem__( self, key, value ):

        self.store[ key ] = value

    def getTempGradient( self ):

        self.store[ 'temp_gradient' ] = -self.store[ 'constants' ][ 'temp_increment' ] * self.store[ 'Alpha' ] * np.cos( self.store[ 'k_polar' ] )

    def transform( self ):
        
        x = self.store[ 'space_radial' ] * np.cos ( self.store[ 'space_azimuthal' ] ) \
                + self.store[ 'Alpha' ] * np.sin( self.store[ 'k_polar' ] ) * np.cos( self.store[ 'k_azimuthal' ] ) 
        y = self.store[ 'space_radial' ] * np.sin ( self.store[ 'space_azimuthal' ] ) \
                + self.store[ 'Alpha' ] * np.sin( self.store[ 'k_polar' ] ) * np.sin( self.store[ 'k_azimuthal' ] ) 
        
        self.store[ 'R_now' ] = np.sqrt( x * x + y * y )
        self.store[ 'P_now' ] = np.arctan2( y, x )
