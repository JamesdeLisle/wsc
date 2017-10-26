import numpy as np
from urt.par import ParamSpace
from gen.lim import Limits
from uti import simpFactor


class LDOS:

    def __init__(self, path0, path1):

        self.lim = Limits()
        self.lim.readData(path0)
        self.P0 = ParamSpace(self.lim, '0', 'gR')
        self.P0.readData(path0)
        self.P1 = ParamSpace(self.lim, '2', 'gR')
        self.P1.readData(path1)

    def compute(self):

        tau3 = np.array([[1, 0], [0, -1]])
        rv = 0.0
        for iXi, Xi in enumerate(self.P0.kPol):
            dosXi = 0.0
            for iTheta, Theta in enumerate(self.P0.kAzi):
                dosTheta = 0.0
                index = (iXi, iTheta)
                g = self.P0.data[self.P0.string][index] \
                    + self.P1.data[self.P1.string][index]
                dosTheta += 1.0 * 1j / (4.0 * np.pi * np.pi)
                dosTheta *= 0.5 * np.trace(np.dot(tau3, g))
                dosTheta *= self.P0.lim.dKAzimu / 3.0
                dosTheta *= simpFactor(iTheta, self.lim.nKAzimu)
                dosXi += np.imag(dosTheta)
            dosXi *= np.sin(Xi) * self.P0.lim.dKPolar / 3.0
            dosXi *= simpFactor(iXi, self.lim.nKPolar)
            rv += dosXi
        return rv
