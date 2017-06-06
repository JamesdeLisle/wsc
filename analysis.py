import space as sp
import ldos
import hcond
import limits as lim
import plotting as plot
from jsci.Coding import NumericEncoder, NumericDecoder
import json

path_data = 'data/gdata.dat'
path_hcond = 'data/hcond.dat'

with open( path_data, 'r' ) as f:
    content = json.loads( f.read(), cls=NumericDecoder )

L = lim.Limits()
L.replaceStore( content[ 'param' ] )

P = sp.ParamSpace( L )
P.readData( path_data )


#A = ldos.LDOS( P )
#A.compute()
#A.writeData( path_ldos )

B = hcond.HCond( P )
B.compute()
B.writeData( path_hcond )

plot.plotLDOS( path_hcond )
