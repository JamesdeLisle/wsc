from gen.par import RunValue, ParamSpaceBase
import numpy as np
import itertools


class ParamSpace(ParamSpaceBase):

    span = None

    def __init__(self, limits, order, string):

        super(ParamSpace, self).__init__(limits, order, string)

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
        rv = []
        for (iXi, Xi), (iTheta, Theta), (iAlpha, Alpha) in DOF:
            values = {'string': string,
                      'order': self.order,
                      'index': (iT, iE, iXi, iTheta, iAlpha),
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
