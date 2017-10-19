import itertools
from gen.par import ParamSpaceBase, RunValue
from jsci.Coding import NumericDecoder
import json
import os
from gen.parser import fileName


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
        rv = list()
        for (iXi, Xi), (iTheta, Theta) in DOF:
            index = (iT, iE, iXi, iTheta)
            values = {'string': string,
                      'order': self.order,
                      'index': index,
                      'temp': self.temp[iT],
                      'ener': self.ener[iE],
                      'Xi': Xi,
                      'Theta': Theta,
                      'lim': self.lim,
                      'dg0': self.dTheta(iXi, iTheta)}
            rv.append(RunValue(**values))

        return rv

    def loadData(self, data_folder, start_time, iT, iE):

        path = os.path.join(data_folder,
                            start_time +
                            fileName('0', self.lim.spinDir, iT, iE))

        with open(path, 'r') as f:
            content = json.loads(f.read(), cls=NumericDecoder)
        self.compData = content['data']['gR']

    def dTheta(self, iXi, iTheta):

        start = iTheta
        if iTheta == self.lim.nKAzimu - 1:
            finish = 0
        else:
            finish = iTheta + 1

        return (self.compData[iXi, start] - self.compData[iXi, finish]) \
            / self.lim.dKAzimu
