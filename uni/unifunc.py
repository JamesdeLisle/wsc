import gen.env as env
import numpy as np


class Uniform:

    def __init__(self, runVal, alpha):

        self.runVal = runVal
        self.envi = env.Environment(runVal)

    @property
    def gR(self):

        V = self.runVal
        E = self.envi

        rv = np.zeros(shape=(2, 2), dtype=np.complex128)
        rv[0, 0] = 1j * V.ener
        rv[1, 1] = -1j * V.ener
        rv -= E.hamR
        rv *= -np.pi / (np.linalg.det(rv))

        return rv

    @property
    def gA(self):

        t3 = np.array([[1, 0], [0, -1]])

        return t3 * self.gR.H * t3

    @property
    def gK(self):

        E = self.envi

        rv = (self.gR - self.gA) * E.thermD

        return rv
