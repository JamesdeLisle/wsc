import gen.env as env
import numpy as np
import gen.forms as fm


class Function:

    def __init__(self, runVal):

        self.runVal = runVal
        self.envi = env.Environment(runVal)

    @property
    def gR1(self):

        V = self.runVal
        E = self.envi

        lam = (V.ener + 1e-6 * 1j) * fm.p3() - E.hamR
        rv = 0.5 * np.linalg.inv(lam) * 1j * V.lim.B_z * V.dg0

        return rv
