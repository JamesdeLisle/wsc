import itertools
from gen.par import ParamSpaceBase, RunValue
from jsci.Coding import NumericDecoder
import json
import os
from gen.parser import fileName


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
            gR = self.compData['0'][iXi, iTheta] \
                + self.compData['2'][iXi, iTheta]
            values = {'string': string,
                      'order': self.order,
                      'index': index,
                      'temp': self.temp[iT],
                      'ener': self.ener[iE],
                      'Xi': Xi,
                      'Theta': Theta,
                      'lim': self.lim,
                      'gK0': self.compData['1'][iXi, iTheta, :],
                      'dgK0': self.dgK0,
                      'gR': gR}
            rv.append(RunValue(**values))

        return rv

    def loadData(self, data_folder, start_time, iT, iE):

        orders = {'0': 'gR', '1': 'gK', '2': 'gR'}
        files = {order: os.path.join(data_folder, start_time +
                                     fileName(order, self.lim.spinDir, iT, iE))
                 for order in orders}

        self.compData = dict()
        for order in orders:
            with open(files[order], 'r') as f:
                content = json.loads(f.read(), cls=NumericDecoder)
                self.compData[order] = content['data'][orders[order]]

    def dTheta(self, iXi, iTheta):

        start = iTheta
        if iTheta == self.lim.nKAzimu - 1:
            finish = 0
        else:
            finish = iTheta + 1

        self.dgK0 = []
        for alpha in range(self.lim.nAlpha):

            self.dgK0.append((self.compData['gK0'][iXi, start, alpha] -
                              self.compData['gK0'][iXi, finish, alpha])
                             / self.lim.dKAzimu)
