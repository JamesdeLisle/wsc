from gen.par import RunValue, ParamSpaceBase
import numpy as np
import itertools


class ParamSpace(ParamSpaceBase):

    span = None

    def __init__(self, limits, order, strings):

        super(ParamSpace, self).__init__(limits, order, strings)

        self.alph = np.linspace(self.lim.alphaMin,
                                self.lim.alphaMax,
                                self.lim.nAlpha)

        self.span = (self.lim.nKPolar,
                     self.lim.nKAzimu,
                     self.lim.nAlpha,
                     2,
                     2)

    def getRun(self, iT, iE, string):
        DOF = itertools.product(enumerate(self.kPol),
                                enumerate(self.kAzi),
                                enumerate(self.alph))
        rv = list()
        for (iXi, Xi), (iTheta, Theta), (iAlpha, Alpha) in DOF:
            index = (iT, iE, iXi, iTheta, iAlpha)
            values = {'string': string,
                      'order': self.order,
                      'index': index,
                      'temp': self.temp[iT],
                      'ener': self.ener[iE],
                      'Xi': Xi,
                      'Theta': Theta,
                      'alpha': Alpha,
                      'lim': self.lim}
            rv.append(RunValue(**values))

        return rv

    def loadData(self, data_folder, start_time, iT, iE):

        pass
