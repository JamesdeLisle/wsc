from gen.par import RunValue, ParamSpaceBase
import itertools


class ParamSpace(ParamSpaceBase):

    span = None

    def __init__(self, limits, order, string):

        super(ParamSpace, self).__init__(limits, order, string)

        self.span = (self.lim.nKPolar,
                     self.lim.nKAzimu,
                     2,
                     2)

    def getRun(self, iT, iE, string):
        DOF = itertools.product(enumerate(self.kPol),
                                enumerate(self.kAzi))
        rv = []
        for (iXi, Xi), (iTheta, Theta) in DOF:
            values = {'string': string,
                      'order': self.order,
                      'index': (iT, iE, iXi, iTheta),
                      'temp': self.temp[iT],
                      'ener': self.ener[iE],
                      'Xi': Xi,
                      'Theta': Theta,
                      'lim': self.lim}
            rv.append(RunValue(**values))

        return rv

    def loadData(self, data_folder, start_time, iT, iE):

        pass
