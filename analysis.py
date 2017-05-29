import space as sp
import ldos
import limits as lim
import plotting as plot
import sanity
from jsci.Coding import NumericEncoder, NumericDecoder
import json

path_data = 'data/gdata.dat'
path_ldos = 'data/ldos.dat'

with open( path_data, 'r' ) as f:
    content = json.loads( f.read(), cls=NumericDecoder )

L = lim.Limits()
L.replaceStore( content[ 'param' ] )

P = sp.ParamSpace( L )
P.readData( path_data )

#S = sanity.Normalisation( P )
#S.compute()

A = ldos.LDOS( P )
A.compute()
A.writeData( path_ldos )

plot.plotLDOS( path_ldos )
