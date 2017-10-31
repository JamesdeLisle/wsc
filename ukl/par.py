from gen.par import RunValue, ParamSpaceBase
import itertools
import os
import json
from jsci.Coding import NumericDecoder
from gen.parser import fileName


class ParamSpace(ParamSpaceBase):

    span = None

    def __init__(self, limits, order, string):

        super(ParamSpace, self).__init__(limits, order, string)

        self.span = (self.lim.nKPolar,
                     self.lim.nKAzimu,
                     2, 2)

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
                      'lim': self.lim,
                      'gR': self.compData['0'][iXi, iTheta]}
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
