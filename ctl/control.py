import main
import numpy as np
import sys
from os.path import join
from gen.parser import nameParser, getFiles
import time
import json
from jsci.Coding import NumericDecoder, NumericEncoder
import itertools


df = 'data/'
sf = 'store'


def updateREG(df, pt, iB, it):
    with open(join(df, 'REG'), 'r') as f:
        REG = json.loads(f.read(), cls=NumericDecoder)['reg']
    REG[iB][it][pt] = True
    with open(join(df, 'REG'), 'w') as f:
        f.write(json.dumps({'reg': REG},
                           cls=NumericEncoder,
                           indent=4))


def checkREG(df, iB, it):
    with open(join(df, 'REG'), 'r') as f:
        REG = json.loads(f.read(), cls=NumericDecoder)['reg']
    return REG[iB][it]['an']


if __name__ == '__main__':
    nb = 50
    nt = 50
    bmin = 0.0
    bmax = 0.3
    tmin = 0.0
    tmax = 0.03
    bSpace = np.linspace(bmin, bmax, nb)
    tSpace = np.linspace(tmin, tmax, nt)
    spin = sys.argv[1]
    if spin == 'up':
        rt = time.strftime('%Y%m%d%H%M%S')
    else:
        rt = nameParser(getFiles(['0'], 'up', df, 'raw')['0'][0], 'run')
    DOF = itertools.product(enumerate(bSpace), enumerate(tSpace))

    pre = (0, 0)
    for (ib, b), (it, t) in DOF:
        if ib or it:
            while not checkREG(df, pre[0], pre[1]):
                time.sleep(5)
            main.Main(spin, b, t, rtval=rt, partial=True)
            pre = (ib, it)
        else:
            main.Main(spin, b, t, rtval=rt, partial=True)
        updateREG(df, spin, ib, it)
