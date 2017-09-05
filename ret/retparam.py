import itertools
from gen.par import ParamSpaceBase, RunValue
from jsci.Coding import NumericDecoder
import json


class ParamSpace(ParamSpaceBase):

    span = None

    def __init__(self, limits, order, strings):

        super(ParamSpace, self).__init__(limits, order, strings)

        self.span = (self.lim.nKPolar,
                     self.lim.nKAzimu,
                     2,
                     2)

    def getRun(self, iT, iE, string):
        DOF = itertools.product(enumerate(self.kPol),
                                enumerate(self.kAzi))
        rv = list()
        for (iXi, Xi), (iTheta, Theta) in DOF:
            index = (iT, iE, iXi, iTheta)
            self.dTheta(iXi, iTheta)
            values = {'string': string,
                      'index': index,
                      'temp': self.temp[iT],
                      'ener': self.ener[iE],
                      'Xi': Xi,
                      'Theta': Theta,
                      'lim': self.lim,
                      'dg0': self.dg0}
            rv.append(RunValue(**values))

        return rv

    def loadData(self, path):

        with open(path, 'r') as f:
            content = json.loads(f.read(), cls=NumericDecoder)
        self.compData = content['data']['gR']

    def dTheta(self, iXi, iTheta):

        start = iTheta
        if iTheta == self.lim.nKAzimu - 1:
            finish = 0
        else:
            finish = iTheta + 1

        self.dg0 = (self.compData[iXi, start, self.lim.nAlpha / 2] -
                    self.compData[iXi, finish, self.lim.nAlpha / 2]) \
            / self.lim.dKAzimu
