import gen.env as env
import numpy as np
import gen.forms as fm


class Function:

    def __init__(self, runVal):

        self.runVal = runVal
        self.envi = env.Environment(runVal)

    @property
    def gR(self):

        V = self.runVal
        E = self.envi

        rv = np.zeros(shape=(2, 2), dtype=np.complex128)
        rv = V.ener * fm.p3()
        rv -= E.hamR
        rv *= -1.0 / np.sqrt((V.ener - E.sigmaR) *
                             (V.ener - E.sigmaR) -
                             np.abs(E.deltaR) *
                             np.abs(E.deltaR))
        return rv
