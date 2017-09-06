import itertools
from gen.par import ParamSpaceBase, RunValue
from jsci.Coding import NumericDecoder
import json
import numpy as np


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
            gR = self.compData['gR0'][iXi, iTheta, self.lim.nAlpha / 2] \
                + self.compData['gR1'][iXi, iTheta]
            values = {'string': string,
                      'index': index,
                      'temp': self.temp[iT],
                      'ener': self.ener[iE],
                      'Xi': Xi,
                      'Theta': Theta,
                      'lim': self.lim,
                      'gK0': self.compData['gK0'][iXi, iTheta, 0],
                      'dgK0': self.dgK0,
                      'gR': gR}
            rv.append(RunValue(**values))

        return rv

    def loadData(self, path_g0, path_gR):

        self.compData = dict()
        with open(path_g0, 'r') as f:
            content = json.loads(f.read(), cls=NumericDecoder)
        self.compData['gR0'] = content['data']['gR']
        self.compData['gK0'] = content['data']['gK']
        with open(path_gR, 'r') as f:
            content = json.loads(f.read(), cls=NumericDecoder)
        self.compData['gR1'] = content['data']['gR1']

    def dTheta(self, iXi, iTheta):

        start = iTheta
        if iTheta == self.lim.nKAzimu - 1:
            finish = 0
        else:
            finish = iTheta + 1

        self.dgK0 = list()
        for alpha in range(self.lim.nAlpha):

            self.dgK0.append((self.compData['gK0'][iXi, start, alpha] -
                              self.compData['gK0'][iXi, finish, alpha])
                             / self.lim.dKAzimu)
