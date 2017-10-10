import gen.env as env
import numpy as np
import gen.forms as fm
import cmath


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
        rv[0, 0] = V.ener + 1e-6 * 1j
        rv[1, 1] = -V.ener - 1e-6 * 1j
        rv -= E.hamR
        rv *= -1.0 / cmath.sqrt(np.dot(rv, rv)[0, 0])
        return rv

    @property
    def gA(self):

        return fm.p3() * np.conj(self.gR).T * fm.p3()

    @property
    def gK(self):

        E = self.envi

        rv = (self.gR - self.gA) * E.thermD

        return rv
