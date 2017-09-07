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
        epsil = 1j * (V.ener - E.sigmaR)

        rv = np.zeros(shape=(2, 2), dtype=np.complex128)
        rv[0, 1] = -E.deltaR - (1j * V.dg0[0, 0]) / (2 * np.conj(E.deltaR))
        rv[1, 0] = np.conj(E.deltaR) + (1j * V.dg0[0, 0]) / (2 * E.deltaR)
        rv[0, 0] = (1.0 / delsq) * (epsil * (2 * delsq + 1j * V.dg0[1, 1])
                                    + np.conj(E.deltaR) * 1j * V.dg0[0, 1])
        rv[1, 1] = (1.0 / delsq) * (-epsil * (2 * delsq + 1j * V.dg0[1, 1])
                                    - np.conj(E.deltaR) * 1j * V.dg0[1, 0])

        return rv
