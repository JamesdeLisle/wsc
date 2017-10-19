import numpy as np
from uni.uniparam import ParamSpace
from gen.lim import Limits


class LDOS:

    def __init__(self, path0, path1):

        self.lim = Limits()
        self.lim.readData(path0)
        self.P0 = ParamSpace(self.lim, '0', ['gR'])
        self.P0.readData(path0)
        self.P1 = ParamSpace(self.lim, '1', ['gR'])
        self.P1.readData(path1)

    def compute(self):

        tau3 = np.array([[1, 0], [0, -1]])
        rv = 0.0
        for iXi, Xi in enumerate(self.P0.kPol):
            dosXi = 0.0
            for iTheta, Theta in enumerate(self.P0.kAzi):
                dosTheta = 0.0
                indexIn0 = (iXi, iTheta, 0)
                indexIn1 = (iXi, iTheta)
                g = self.P0.data[self.P0.strings[0]][indexIn0] \
                    -  1j *self.P1.data[self.P1.strings[0]][indexIn1]
                dosTheta += 1.0 * 1j / (4.0 * np.pi * np.pi)
                dosTheta *= 0.5 * np.trace(np.dot(tau3, g))
                dosTheta *= self.P0.lim.dKAzimu / 3.0
                if iTheta == 0 or iTheta == self.P0.lim.nKAzimu:
                    pass
                elif iTheta % 2 == 0:
                    dosTheta *= 4.0
                else:
                    dosTheta *= 2.0
                dosXi += np.imag(dosTheta)

            dosXi *= np.sin(Xi) * self.P0.lim.dKPolar / 3.0
            if iXi == 0 or iXi == self.P0.lim.nKPolar:
                pass
            elif iXi % 2 == 0:
                dosXi *= 4.0
            else:
                dosXi *= 2.0
            rv += dosXi
        return rv
