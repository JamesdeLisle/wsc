import gen.env as envi
import numpy as np
import gen.forms as fm


class Quantum:

    def __init__(self, runVal, funcVal):

        self.runVal = runVal
        self.runVal.compSpace()
        self.funcVal = funcVal
        self.envi = envi.Environment(runVal)

    @property
    def Qf(self):

        V = self.runVal
        E = self.envi

        epsil = V.ener * fm.p3()
        gA = np.dot(np.dot(fm.p3(), np.conj(V.gR).T), fm.p3())
        dpzgA1 = np.dot(np.dot(fm.p3(), np.conj(V.dpzgR1).T), fm.p3())
        rv = np.dot((epsil - E.hamR), self.funcVal) \
            - np.dot(self.funcVal, (epsil - E.hamA)) \
            + np.dot(V.gR, E.hamKG) \
            - np.dot(E.hamKG, gA) \
            - (1j / 2.0) * np.dot(V.dpzgR1, E.dzhamKG) \
            - (1j / 2.0) * np.dot(E.dzhamKG, dpzgA1)

        return -rv / V.lim.v
