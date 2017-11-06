import itertools
from gen.par import ParamSpaceBase, RunValue
from jsci.Coding import NumericDecoder
import json
import os
from gen.parser import fileName
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
            self.dgR0(iXi, iTheta)
            gR = self.compData['0'][iXi, iTheta]
            values = {'string': string,
                      'order': self.order,
                      'index': (iT, iE, iXi, iTheta),
                      'temp': self.temp[iT],
                      'ener': self.ener[iE],
                      'Xi': Xi,
                      'Theta': Theta,
                      'lim': self.lim,
                      'dpzgR0': self.dpzgR0,
                      'gR': gR}
            rv.append(RunValue(**values))

        return rv

    def loadData(self, data_folder, start_time, iT, iE):

        orders = {'0': 'gR'}
        files = {order: os.path.join(data_folder, start_time +
                                     fileName(order, self.lim.spinDir, iT, iE))
                 for order in orders}

        self.compData = dict()
        for order in orders:
            with open(files[order], 'r') as f:
                content = json.loads(f.read(), cls=NumericDecoder)
                self.compData[order] = content['data'][orders[order]]

    def dgR0(self, iXi, iTheta):

        start = iXi
        if iXi == self.lim.nKPolar - 1:
            finish = 0
        else:
            finish = iXi + 1

        self.dpzgR0 = (self.compData['0'][iXi, start] -
                       self.compData['0'][iXi, finish]) / self.lim.dKPolar
        self.dpzgR0 /= -self.lim.v
        self.dpzgR0 *= np.sin(self.kPol[iXi])
