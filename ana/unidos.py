import numpy as np
from urt.par import ParamSpace
from gen.lim import Limits
import gen.forms as fm
from uti import simpFactor


class LDOS:

    def __init__(self, path, order, func):

        self.path = path
        self.order = order
        self.func = func
        self.lim = Limits()
        self.lim.readData(self.path)
        self.P = ParamSpace(self.lim, order, func)
        self.P.readData(self.path)

    def compute(self):

        rv = 0.0
        for iXi, Xi in enumerate(self.P.kPol):
            dosXi = 0.0
            for iTheta, Theta in enumerate(self.P.kAzi):
                dosTheta = 0.0
                indexIn = (iXi, iTheta)
                g = self.P.data[self.P.string][indexIn]
                dosTheta += 1.0 * 1j / (4.0 * np.pi * np. pi)
                dosTheta *= 0.5 * np.trace(np.dot(fm.p3(), g))
                dosTheta *= self.P.lim.dKAzimu / 3.0
                dosTheta *= simpFactor(iTheta, self.lim.nKAzimu)
                dosXi += np.imag(dosTheta)
            dosXi *= np.sin(Xi) * self.P.lim.dKPolar / 3.0
            dosXi *= simpFactor(iXi, self.lim.nKPolar)
            rv += dosXi
        return rv
