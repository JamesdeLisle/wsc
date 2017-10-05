import gen.env as env
import numpy as np
import uni.unifunc as unif


class Function:

    def __init__(self, runVal):

        self.runVal = runVal
        self.envi = env.Environment(runVal)

    @property
    def gR1(self):

        V = self.runVal
        E = self.envi

        tau3 = np.eye(2)
        tau3[1, 1] = -1.0
        lam = V.ener * tau3 - E.hamR
        rv = 0.5 * np.linalg.inv(lam) * 1j * V.lim.B_z * V.dg0

        return rv
