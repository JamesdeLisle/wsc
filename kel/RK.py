import kelfunc as kelf
import numpy as np


class RK:

    def __init__(self, runVal):

        self.runVal = runVal
        self.alphaSpa = np.linspace(self.valSet.lim.alphaMin,
                                    self.valSet.lim.alphaMax,
                                    self.valSet.lim.nAlpha)
        self.funcVal = self.valSet.gK0[0]
        self.runVal.alpha = 0
        self.dAlpha = self.runVal.lim.dAlpha
        self.kInc = [np.zeros(shape=(2, 2)) for x in range(4)]

    @property
    def gK1(self):

        for iAlpha, alpha in enumerate(self.alphaSpa):

            self.runVal.iAlpha = iAlpha
            func = kelf.Keldysh(self.runVal, self.funcVal)
            self.kInc[0] = func.fK1

            self.runVal.iAlpha = iAlpha + self.dAlpha
            func = kelf.Keldysh(self.runVal,
                                self.funcVal + self.dAlpha * self.kInc[0] / 2)
            self.kInc[1] = func.fK1

            func = kelf.Keldysh(self.runVal,
                                self.funcVal + self.dAlpha * self.kInc[1] / 2)
            self.kInc[2] = func.fK1

            self.runVal.iAlpha = iAlpha + 1
            func = kelf.Keldysh(self.runVal,
                                self.funcVal + self.dAlpha * self.kInc[2])
            self.kInc[3] = func.fK1

            self.funcVal += self.dAlpha * (self.kInc[0]
                                           + 2 * (self.kInc[1] + self.kInc[2])
                                           + self.kInc[3]) / 6

        return self.funcVal
