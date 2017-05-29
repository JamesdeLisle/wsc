import numpy as np
import itertools
import warnings

warnings.filterwarnings( 'error' )

def delta( R, Phi, Xi, Theta, T, T_c ):

    a = 1.764 / ( 2 * np.pi )
    b = np.tanh( np.sqrt( T_c / T - 1 ) ) 
    c = np.tanh( R ) * np.exp( 1j * Phi )
    d = np.sin( Xi ) * np.exp( 1j * Theta )

    return a * b * c * d

def tranR( R, Phi, Xi, Theta, Alpha ):

    x = R * np.cos( Phi ) + Alpha * np.sin( Xi ) * np.cos( Theta )
    y = R * np.sin( Phi ) + Alpha * np.sin( Xi ) * np.sin( Theta )

    return np.sqrt( x * x + y * y )

def tranPhi( R, phi, xi, theta, alpha ):

    x = R * np.cos( phi ) + alpha * np.sin( xi ) * np.cos( Theta )
    y = R * np.sin( phi ) + alpha * np.sin( xi ) * np.sin( Theta )

    return np.arctan2( y, x )

def FgamR( E, sigR, delta, gamR ):

    return 1j * ( 2 * E * gamR \
            - sigR * gamR \
            + np.conj( sigR ) * gamR \
            + gamR * gamR * np.conj( delta ) \
            + delta )

def FgamR_B( E, sigR, delta, gamR ):

    return 1j * ( -2 * E * gamR \
            - np.conj( sigR ) * gamR \
            + sigR * gamR \
            + gamR * gamR * delta \
            + np.conj( delta ) )

def boundR( delta, sigR, E ):
    
    epsilon = E - ( sigR - np.conj( sigR ) ) / 2
    return -delta / ( epsilon + 1j * np.sqrt( delta * np.conj( delta ) - epsilon * epsilon ) )

def boundR_B( delta, sigR, E ):
    
    epsilon = E - ( sigR - np.conj( sigR ) ) / 2
    return np.conj( delta ) / ( epsilon + 1j * np.sqrt( delta * np.conj( delta ) - epsilon * epsilon ) )

nTheta = 30
nXi = 15
nR = 10
nPhi = 5
T_c = 1.0
T = 0.1
E = 0.0

sigR = -1j * 0.01

Alpha_limit = 10.0
ADisc = [ 10.0/50, -10.0/50 ]

Alpha = [0.0,0.0]
RAlpha = [0.0,0.0]
PAlpha = [0.0,0.0]
Delta = [0.0,0.0 ]

Theta_list = np.linspace( 0, 2*np.pi, nTheta )
Xi_list = np.linspace( 0, np.pi, nXi)
R_list = np.linspace( 0, 5.0, nR )
Phi_list = np.linspace( 0, 2*np.pi, nPhi )

GAMMA = [ np.zeros( shape=(nR, nPhi, nXi, nTheta ), dtype=np.complex64 ) for x in range(2) ]

k = [ [0,0,0,0],[0,0,0,0]]

for iR,R in enumerate(R_list):
    for iPhi, Phi in enumerate(Phi_list):
        for iXi, Xi in enumerate( Xi_list):
            for iTheta, Theta in enumerate(Theta_list):
                Alpha[0] = -Alpha_limit
                Alpha[1] = Alpha_limit
                
                RAlpha[0] = tranR( R, Phi, Xi, Theta, Alpha[0] ) 
                PAlpha[0] = tranPhi( R, Phi, Xi, Theta, Alpha[0] ) 
                RAlpha[1] = tranR( R, Phi, Xi, Theta, Alpha[1] ) 
                PAlpha[1] = tranPhi( R, Phi, Xi, Theta, Alpha[1] ) 
                Delta[0] = delta( RAlpha[0], PAlpha[0], Xi, Theta, T, T_c )
                Delta[1] = delta( RAlpha[1], PAlpha[1], Xi, Theta, T, T_c )
                GAMMA[0][iR,iPhi,iXi,iTheta] = boundR( Delta[0], sigR, E )
                GAMMA[1][iR,iPhi,iXi,iTheta] = boundR_B( Delta[1], sigR, E )
                EPS = E - ( sigR - np.conj( sigR ) ) / 2
                if ( iR, iPhi, iXi, iTheta ) == ( 0,2,7,13 ):           

                    print '####################'

                #print '\n'

                for i in range( 50 ):
                    
                    k[0][0] = FgamR( E, sigR, Delta[0], GAMMA[0][iR,iPhi,iXi,iTheta] )
                    if ( iR, iPhi, iXi, iTheta ) == ( 0,2,7,13 ):
                        print  k[0][0]
                    RAlpha[0] = tranR( R, Phi, Xi, Theta, Alpha[0]+ADisc[0]/2 ) 
                    PAlpha[0] = tranPhi( R, Phi, Xi, Theta, Alpha[0]+ADisc[0]/2 )
                    Delta[0] = delta( RAlpha[0], PAlpha[0], Xi, Theta, T, T_c )
                    k[0][1] = FgamR( E, sigR, Delta[0], GAMMA[0][iR,iPhi,iXi,iTheta]+ADisc[0]*k[0][0]/2 )
                    k[0][2] = FgamR( E, sigR, Delta[1], GAMMA[0][iR,iPhi,iXi,iTheta]+ADisc[0]*k[0][1]/2 )
                    RAlpha[0] = tranR( R, Phi, Xi, Theta, Alpha[0]+ADisc[0] ) 
                    PAlpha[0] = tranPhi( R, Phi, Xi, Theta, Alpha[0]+ADisc[0] ) 
                    Delta[0] = delta( RAlpha[0], PAlpha[0], Xi, Theta, T, T_c )
                    k[0][3] = FgamR( E, sigR, Delta[0], GAMMA[0][iR,iPhi,iXi,iTheta]+ADisc[0]*k[0][2] )
                    Alpha[0] += ADisc[0] 

                    k[1][0] = FgamR_B( E, sigR, Delta[1], GAMMA[1][iR,iPhi,iXi,iTheta] )
                    RAlpha[1] = tranR( R, Phi, Xi, Theta, Alpha[1]+ADisc[1]/2 ) 
                    PAlpha[1] = tranPhi( R, Phi, Xi, Theta, Alpha[1]+ADisc[1]/2 )
                    Delta[1] = delta( RAlpha[1], PAlpha[1], Xi, Theta, T, T_c )
                    k[1][1] = FgamR_B( E, sigR, Delta[1], GAMMA[1][iR,iPhi,iXi,iTheta]+ADisc[1]*k[1][0]/2 )
                    k[1][2] = FgamR_B( E, sigR, Delta[1], GAMMA[1][iR,iPhi,iXi,iTheta]+ADisc[1]*k[1][1]/2 )
                    RAlpha[1] = tranR( R, Phi, Xi, Theta, Alpha[1]+ADisc[1] ) 
                    PAlpha[1] = tranPhi( R, Phi, Xi, Theta, Alpha[1]+ADisc[1] )
                    Delta[1] = delta( RAlpha[1], PAlpha[1], Xi, Theta, T, T_c )
                    k[1][3] = FgamR_B( E, sigR, Delta[1], GAMMA[1][iR,iPhi,iXi,iTheta]+ADisc[1]*k[1][2] )
                    Alpha[1] += ADisc[1]
                    #if ( iR, iPhi, iXi, iTheta ) == ( 0,2,7,13 ):
                     #   print k[ 0 ]

                    GAMMA[0][iR,iPhi,iXi,iTheta] += ( ADisc[0] / 6.0 ) * ( k[0][0] + 2 * ( k[0][1] + k[0][2] ) + k[0][3] )
                    GAMMA[1][iR,iPhi,iXi,iTheta] += ( ADisc[1] / 6.0 ) * ( k[1][0] + 2 * ( k[1][1] + k[1][2] ) + k[1][3] )
                if ( iR, iPhi, iXi, iTheta ) == ( 0,2,7,13 ):
                    print GAMMA[0][iR,iPhi,iXi,iTheta]
                    print GAMMA[1][iR,iPhi,iXi,iTheta]

        print iR, iPhi


    
LDOS = np.zeros( shape=( nR, nPhi ) )

dtheta = 2*np.pi/nTheta
dxi = np.pi/nXi
degrees_of_freedom = itertools.product( enumerate( R_list ), \
                                        enumerate( Phi_list ) )
 
for ( iR, R ), ( iphi, phi ) in degrees_of_freedom:
    index_out = ( iR, iphi )
    for ixi, xi in enumerate( Xi_list ):
        dosXi = 0.0
        for itheta, theta in enumerate( Theta_list ):
            dosTh = 0.0
            index_in = ( iR, iphi, ixi, itheta )
            dosTh = 1j * 1.0 / ( 4.0 * np.pi )
            dosTh = dosTh * ( 1 - GAMMA[0][ index_in ] * GAMMA[1][index_in] )
            dosTh = dosTh / ( 1 + GAMMA[0][ index_in ] * GAMMA[1][index_in] )
            dosTh = dosTh * dtheta / 3.0
            if itheta == 0 or itheta == nTheta:
                pass
            elif itheta % 2 == 0:
                dosTh = dosTh * 4.0
            else:
                dosTh = dosTh * 2.0
            dosXi = dosXi + float( np.imag ( dosTh ) )
        dosXi = dosXi * np.sin( xi ) * dxi / 3.0
        if ixi == 0 or ixi == nXi:
            pass
        elif ixi % 2 == 0:
            dosXi = dosXi * 4.0
        else:
            dosXi = dosXi * 2.0
        LDOS[ index_out ] += dosXi 

degrees_of_freedom = itertools.product( enumerate( R_list ), \
                                        enumerate( Phi_list ) )
with open( 'LDOS.dat', 'w' ) as f:
    for ( iR, R ), ( iphi, phi ) in degrees_of_freedom:
        f.write( '%f %f %f %f %f\n' % ( T, E, R, phi, LDOS[ iR, iphi ] ) )
f.close()





