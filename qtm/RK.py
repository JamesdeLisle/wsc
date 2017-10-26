import qtmfunc as qtmf
import numpy as np
import bound


class Function:

    def __init__(self, runVal):

        self.runVal = runVal
        self.alphaSpa = np.linspace(self.runVal.lim.alphaMin,
                                    self.runVal.lim.alphaMax,
                                    self.runVal.lim.nAlpha)
        self.runVal.alpha = self.alphaSpa[0]
        BC = bound.Function(self.runVal)
        self.funcVal = BC.gK
        self.runVal.alpha = 0
        self.dAlpha = self.runVal.lim.dAlpha
        self.kInc = [np.zeros(shape=(2, 2)) for x in range(4)]

    @property
    def gK(self):

        for iAlpha, alpha in enumerate(self.alphaSpa[0:-1]):

            self.runVal.iAlpha = iAlpha
            self.runVal.alpha = alpha
            func = qtmf.Quantum(self.runVal, self.funcVal)
            self.kInc[0] = func.Qf

            self.runVal.iAlpha = iAlpha + self.dAlpha / 2
            self.runVal.alpha = alpha + self.dAlpha / 2
            func = qtmf.Quantum(self.runVal,
                                self.funcVal + self.dAlpha * self.kInc[0] / 2)
            self.kInc[1] = func.Qf

            func = qtmf.Quantum(self.runVal,
                                self.funcVal + self.dAlpha * self.kInc[1] / 2)
            self.kInc[2] = func.Qf

            self.runVal.iAlpha = iAlpha + 1
            self.runVal.alpha = alpha + self.dAlpha
            func = qtmf.Quantum(self.runVal,
                                self.funcVal + self.dAlpha * self.kInc[2])
            self.kInc[3] = func.Qf

            self.funcVal += self.dAlpha * (self.kInc[0]
                                           + 2 * (self.kInc[1] + self.kInc[2])
                                           + self.kInc[3]) / 6

        return self.funcVal
