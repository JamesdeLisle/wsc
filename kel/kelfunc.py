import gen.env as envi
import numpy as np
from math import ceil


class Keldysh:

    def __init__(self, runVal, funcVal):

        self.runVal = runVal
        self.runVal.compSpace()
        self.funcVal = funcVal
        self.envi = envi.Environment(runVal)

    @property
    def fK1(self):

        V = self.runVal
        E = self.envi

        tau3 = np.array([[1, 0], [0, -1]])
        epsil = np.zeros(shape=(2, 2), dtype=np.complex128)
        epsil[0, 0] = V.ener
        epsil[1, 1] = -V.ener
        gA = tau3 * np.conj(V.gR).T * tau3

        if type(self.runVal.iAlpha) == int:
            dgK0 = V.dgK0[self.runVal.iAlpha]
        else:
            dgK0 = (V.dgK0[int(self.runVal.iAlpha)]
                    + V.dgK0[int(ceil(self.runVal.iAlpha))]) / 2

        rv = (epsil - E.hamR) * self.funcVal \
            - self.funcVal * (epsil - E.hamA) \
            + V.gR * E.hamK \
            - E.hamK * gA \
            + 1j * V.lim.B_z * dgK0

        return rv
