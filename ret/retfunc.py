import gen.env as env
import numpy as np


class Function:

    def __init__(self, runVal):

        self.runVal = runVal
        self.envi = env.Environment(runVal)

    @property
    def gR1(self):

        V = self.runVal
        E = self.envi

        delsq = np.abs(E.deltaR) * np.abs(E.deltaR)
        epsil = V.ener + 1j * 1e-6 - E.sigmaR

        rv = np.zeros(shape=(2, 2), dtype=np.complex128)
        rv[0, 1] = -E.deltaR * (1 - V.dg0[0, 0] / (2 * np.conj(E.deltaR)))
        rv[1, 0] = np.conj(E.deltaR) * (1 + V.dg0[0, 0] / (2 * E.deltaR))
        rv[0, 0] = 1j * (2 * epsil * rv[0, 1] - V.lim.B_z * V.dg0[0, 1]) / \
            (2 * E.deltaR)
        rv[1, 1] = -1j * (2 * epsil * rv[1, 0] + V.lim.B_z * V.dg0[1, 0]) / \
            (2 * np.abs(E.deltaR))

        return rv
