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

        lam = V.ener * fm.p3() - E.hamR
        if self.runVal.Xi < np.pi / 2:
            sgn = 1.0
        else:
            sgn = -1.0
        rv = -np.dot(0.5 * np.linalg.inv(lam), sgn * 1j * V.lim.B_z * V.dg0)
        return rv
