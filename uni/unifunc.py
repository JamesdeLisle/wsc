import gen.env as env
import numpy as np


class Function:

    def __init__(self, runVal):

        self.runVal = runVal
        self.runVal.compSpace()
        self.envi = env.Environment(runVal)

    @property
    def gR(self):

        V = self.runVal
        E = self.envi

        rv = np.zeros(shape=(2, 2), dtype=np.complex128)
        rv[0, 0] = V.ener
        rv[1, 1] = -V.ener
        rv -= E.hamR
        rv *= -1.0 / np.sqrt((V.ener - E.sigmaR) *
                             (V.ener - E.sigmaR) -
                             np.abs(E.deltaR) *
                             np.abs(E.deltaR))
        return rv

    @property
    def gA(self):

        t3 = np.array([[1, 0], [0, -1]])

        return t3 * np.conj(self.gR).T * t3

    @property
    def gK(self):

        E = self.envi

        rv = (self.gR - self.gA) * E.thermD

        return rv
