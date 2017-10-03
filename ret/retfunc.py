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

        delsq = E.deltaR * np.conj(E.deltaR)
        epsil = V.ener + 1j * 1e-6 - E.sigmaR
        if V.Theta < 0.0:
            bsign = 1.0
        else:
            bsign = -1.0

        f = E.deltaR * (1 - 1j * V.lim.B_z * bsign * V.dg0[0, 0] / (2 * delsq))
        f_bar = -np.conj(E.deltaR) * (1 - 1j * V.lim.B_z * bsign * V.dg0[1, 1] /
                                      (2 * delsq))
        if V.Theta < 0.0:
            bsign = -1.0
        else:
            bsign = 1.0

        rv = np.zeros(shape=(2, 2), dtype=np.complex128)
        rv[0, 1] = f
        rv[1, 0] = f_bar
        rv[0, 0] = (1.0 / (2 * E.deltaR)) \
            * (-2 * epsil * f + 1j * V.lim.B_z * bsign * V.dg0[0, 1])
        rv[1, 1] = -rv[0, 0]

        return rv
