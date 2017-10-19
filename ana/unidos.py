import numpy as np
from uni.uniparamret import ParamSpace
from gen.lim import Limits
import gen.forms as fm


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
                if iTheta == 0 or iTheta == self.P.lim.nKAzimu:
                    pass
                elif iTheta % 2 == 0:
                    dosTheta *= 4.0
                else:
                    dosTheta *= 2.0
                dosXi += np.imag(dosTheta)

            dosXi *= np.sin(Xi) * self.P.lim.dKPolar / 3.0
            if iXi == 0 or iXi == self.P.lim.nKPolar:
                pass
            elif iXi % 2 == 0:
                dosXi *= 4.0
            else:
                dosXi *= 2.0
            rv += dosXi
        return rv
