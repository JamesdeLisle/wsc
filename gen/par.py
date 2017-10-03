import numpy as np
import json
from jsci.Coding import NumericEncoder, NumericDecoder
from abc import ABCMeta, abstractproperty, abstractmethod
import sys


class RunValue:

    def __init__(self, *args, **kwargs):

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def compSpace(self):

        x = self.alpha * np.sin(self.Xi) * np.cos(self.Theta)
        y = self.alpha * np.sin(self.Xi) * np.sin(self.Theta)

        self.R = np.sqrt(x * x + y * y)
        self.Phi = np.arctan2(y, x)
        self.Z = self.alpha * np.cos(self.Xi)


class ParamSpaceBase(object):

    __metaclass__ = ABCMeta

    def __init__(self, limits, order, strings):

        self.lim = limits
        self.order = order
        self.strings = strings
        self.temp = np.linspace(self.lim.tempMin,
                                self.lim.tempMax,
                                self.lim.nTemp)
        self.ener = np.linspace(self.lim.energyMin,
                                self.lim.energyMax,
                                self.lim.nEnergy)
        self.kPol = np.linspace(self.lim.kPolarMin,
                                self.lim.kPolarMax,
                                self.lim.nKPolar)
        self.kAzi = np.linspace(self.lim.kAzimuMin,
                                self.lim.kAzimuMax,
                                self.lim.nKAzimu)

    @abstractproperty
    def span(self):
        pass

    @abstractmethod
    def getRun(self, iT, iE, string):
        pass

    @abstractmethod
    def loadData(self, data_folder, start_time, iT, iE):
        pass

    def initData(self, label):

        self.label = label
        self.data = {string: np.zeros(shape=self.span, dtype=np.complex128)
                     for string in self.strings}

    def updateData(self, data, string):
        try:
            for value in data:
                index = value['index'][2:len(value['index'])]
                self.data[string][index] = value['value']
        except AttributeError:
            print('You have not run the initData method.')
            sys.exit()

    def writeData(self, path):
        try:
            path_complete = path + '-%s-T%03dE%03d' % (self.order,
                                                       self.label[0],
                                                       self.label[1])
            with open(path_complete, 'w') as f:
                f.write(json.dumps({'param': self.lim.save(),
                                    'data': self.data},
                                   cls=NumericEncoder,
                                   indent=4,
                                   sort_keys=True))
        except AttributeError:
            print('You have either not run run updateData')
            sys.exit()

    def readData(self, path):

        with open(path, 'r') as f:
            content = json.loads(f.read(), cls=NumericDecoder)
        self.data = content['data']
        self.label = (int(path[-7:-4]), int(path[-3:]))

    def getProgress(self, iT, iE):

        perc = 100 * (float(iT * self.lim.nEnergy) + iE) / \
               (self.lim.nTemp * self.lim.nEnergy)
        if iT == self.lim.nTemp - 1 and iE == self.lim.nEnergy - 1:
            sys.stdout.write('\r100%    ')
        else:
            sys.stdout.write('\r%.2f%%' % perc)
        sys.stdout.flush()
