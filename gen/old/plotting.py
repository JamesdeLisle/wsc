from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import numpy as np

def plotLDOS( path ):

    fig = plt.figure()
    ax = fig.add_subplot( 111, projection='3d' )

    R = []
    P = []
    Z = []
    with open( path, 'r' ) as f:
        for line in f:
            words = line.split()
            R.append( float( words[2] ) )
            P.append( float( words[3] ) )
            Z.append( float( words[4] ) )

    X = [ r*np.cos( p ) for r,p in zip( R, P ) ]
    Y = [ r*np.sin( p ) for r,p in zip( R, P ) ]
    ax.scatter( X, Y, Z, c='r', marker='o')
    ax.set_zlim( [0.0, max( Z ) ] )
    plt.show()
