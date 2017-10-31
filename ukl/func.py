import gen.env as env
import numpy as np
import gen.forms as fm


class Keldysh:

    def __init__(self, runVal, funcVal):

        self.runVal = runVal
        self.runVal.compSpace()
        self.funcVal = funcVal
        self.envi = env.Environment(runVal)

    @property
    def fK0(self):

        V = self.runVal
        E = self.envi

        epsil = np.zeros(shape=(2, 2), dtype=np.complex128)
        epsil[0, 0] = V.ener
        epsil[1, 1] = -V.ener
        gA = np.dot(np.dot(fm.p3(), np.conj(V.gR).T), fm.p3())

        rv = np.dot((epsil - E.hamR), self.funcVal) \
            - np.dot(self.funcVal, (epsil - E.hamA)) \
            + np.dot(V.gR, E.hamKG) \
            - np.dot(E.hamKG, gA)
        return -rv / V.lim.v
