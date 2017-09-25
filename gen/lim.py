import numpy as np
import json
from jsci.Coding import NumericDecoder


class Limits(object):

    def __init__(self):

        """manually set limits"""
        self._spinDir = None
        self._nEnergy = None
        self._nKPolar = None
        self._nKAzimu = None
        self._nTemp = None
        self._nAlpha = None
        self._energyMin = None
        self._energyMax = None
        self._kPolarMin = None
        self._kPolarMax = None
        self._kAzimuMin = None
        self._kAzimuMax = None
        self._T_c = None
        self._tempMin = None
        self._tempMax = None
        self._tempInc = None
        self._alphaMin = None
        self._alphaMax = None
        self._a1 = None
        self._a2 = None
        self._a3 = None
        self._a4 = None
        self._B_z = None
        self._tau = None

        """automatically computed limits"""
        self._dEnergy = None
        self._dKPolar = None
        self._dKAzimu = None
        self._dTemp = None
        self._dAlpha = None
        self._gamma1 = None
        self._gamma2 = None

        self.goFlag = False

    def finalise(self):

        self.compute_dEnergy()
        self.compute_dKPolar()
        self.compute_dKAzimu()
        self.compute_dTemp()
        self.compute_dAlpha()
        self.compute_gamma1()
        self.compute_gamma2()

        self.goFlag = True

    def save(self):

        rv = dict()
        rv['spinDir'] = self.spinDir
        rv['nEnergy'] = self.nEnergy
        rv['nKPolar'] = self.nKPolar
        rv['nKAzimu'] = self.nKAzimu
        rv['nTemp'] = self.nTemp
        rv['nAlpha'] = self.nAlpha
        rv['energyMin'] = self.energyMin
        rv['energyMax'] = self.energyMax
        rv['kPolarMin'] = self.kPolarMin
        rv['kPolarMax'] = self.kPolarMax
        rv['kAzimuMin'] = self.kAzimuMin
        rv['kAzimuMax'] = self.kAzimuMax
        rv['T_c'] = self.T_c
        rv['tempMin'] = self.tempMin
        rv['tempMax'] = self.tempMax
        rv['tempInc'] = self.tempInc
        rv['alphaMin'] = self.alphaMin
        rv['alphaMax'] = self.alphaMax
        rv['a1'] = self.a1
        rv['a2'] = self.a2
        rv['a3'] = self.a3
        rv['a4'] = self.a4
        rv['B_z'] = self.B_z

        return rv

    def load(self, values):

        for key, value in values.iteritems():
            setattr(self, key, value)

    def readData(self, path):

        with open(path, 'r') as f:
            content = json.loads(f.read(), cls=NumericDecoder)
        self.load(content['param'])
        self.finalise()

    @property
    def spinDir(self):
        if self._spinDir:
            return self._spinDir
        else:
            raise RuntimeError('spinDir has not been defined.')

    @spinDir.setter
    def spinDir(self, value):
        if value in ['up', 'down']:
            self._spinDir = value
        else:
            raise ValueError("The spin direction must be 'up' or 'down'")

    @property
    def nEnergy(self):
        if self._nEnergy:
            return self._nEnergy
        else:
            raise RuntimeError('nEnergy has not been defined.')

    @nEnergy.setter
    def nEnergy(self, value):
        if type(value) == int and \
           value > 0:
            self._nEnergy = value
        else:
            raise ValueError('The Energy discretisation '
                             + 'must be a positive integer.')

    @property
    def nKPolar(self):
        if self._nKPolar:
            return self._nKPolar
        else:
            raise RuntimeError('nKPolar has not been defined.')

    @nKPolar.setter
    def nKPolar(self, value):
        if type(value) == int and \
           value > 0:
            self._nKPolar = value
        else:
            raise ValueError('The polar momentum discretisation '
                             + 'must be a positive integer.')

    @property
    def nKAzimu(self):
        if self._nKAzimu:
            return self._nKAzimu
        else:
            raise RuntimeError('nKAzimu has not been defined.')

    @nKAzimu.setter
    def nKAzimu(self, value):
        if type(value) == int and \
           value > 0:
            self._nKAzimu = value
        else:
            raise ValueError('The azimuthal momentum discretisation '
                             + 'must be a positive integer.')

    @property
    def nTemp(self):
        if self._nTemp:
            return self._nTemp
        else:
            raise RuntimeError('nTemp has not been defined.')

    @nTemp.setter
    def nTemp(self, value):
        if type(value) == int and \
           value > 0:
            self._nTemp = value
        else:
            raise ValueError('The temperature discretisation '
                             + 'must be a positive integer.')

    @property
    def nAlpha(self):
        if self._nAlpha:
            return self._nAlpha
        else:
            raise RuntimeError('nAlpha has not been defined')

    @nAlpha.setter
    def nAlpha(self, value):
        if type(value) == int and \
           value > 0:
            self._nAlpha = value
        else:
            raise ValueError('The alpha discretisation '
                             + 'must be a positive integer.')

    @property
    def energyMin(self):
        if self._energyMin:
            return self._energyMin
        else:
            raise RuntimeError('energyMin has not been defined')

    @energyMin.setter
    def energyMin(self, value):
        if type(value) == float:
            self._energyMin = value
        else:
            raise ValueError('The minimum energy must be a float.')

    @property
    def energyMax(self):
        if self._energyMax:
            return self._energyMax
        else:
            raise RuntimeError('energyMax has not been defined.')

    @energyMax.setter
    def energyMax(self, value):
        if type(value) == float:
            self._energyMax = value
        else:
            raise ValueError('The maximum energy must be a float.')

    @property
    def kPolarMin(self):
        if self._kPolarMin or self._kPolarMin == 0.0:
            return self._kPolarMin
        else:
            raise RuntimeError('kPolarMin has not been defined.')

    @kPolarMin.setter
    def kPolarMin(self, value):
        if type(value) == float:
            self._kPolarMin = value
        else:
            raise ValueError('The minimum kPolar must be a float.')

    @property
    def kPolarMax(self):
        if self._kPolarMax:
            return self._kPolarMax
        else:
            raise RuntimeError('kPolarMax has not been defined.')

    @kPolarMax.setter
    def kPolarMax(self, value):
        if type(value) == float:
            self._kPolarMax = value
        else:
            raise ValueError('The maximum kPolar must be a float.')

    @property
    def kAzimuMin(self):
        if self._kAzimuMin or self._kAzimuMin == 0.0:
            return self._kAzimuMin
        else:
            raise RuntimeError('kAzimuMin has not been defined.')

    @kAzimuMin.setter
    def kAzimuMin(self, value):
        if type(value) == float:
            self._kAzimuMin = value
        else:
            raise ValueError('The minimum kAzimu must be a float.')

    @property
    def kAzimuMax(self):
        if self._kAzimuMax:
            return self._kAzimuMax
        else:
            raise RuntimeError('kAzimuMax has not been defined')

    @kAzimuMax.setter
    def kAzimuMax(self, value):
        if type(value) == float:
            self._kAzimuMax = value
        else:
            raise ValueError('The maximum kAzimu must be a float.')

    @property
    def T_c(self):
        if self._T_c:
            return self._T_c
        else:
            raise RuntimeError('T_c has not been defined')

    @T_c.setter
    def T_c(self, value):
        if type(value) == float and \
           value > 0.0:
            self._T_c = value
        else:
            raise ValueError('The critical temperature must ' +
                             'be a positive float.')

    @property
    def tempMin(self):
        if self._tempMin or self._tempMin == 0.0:
            return self._tempMin
        else:
            raise RuntimeError('tempMin has not beed defined')

    @tempMin.setter
    def tempMin(self, value):
        if type(value) == float and \
           value >= 0.0:
            self._tempMin = value
        else:
            raise ValueError('The minimum temp must be a positive float.')

    @property
    def tempMax(self):
        if self._tempMax:
            return self._tempMax
        else:
            raise RuntimeError('tempMax has not been defined')

    @tempMax.setter
    def tempMax(self, value):
        if type(value) == float and \
           value > 0.0:
            self._tempMax = value
        else:
            raise ValueError('The maximum temp must be a positive float.')

    @property
    def tempInc(self):
        if self._tempInc:
            return self._tempInc
        else:
            raise RuntimeError('tempInc has not been defined')

    @tempInc.setter
    def tempInc(self, value):
        if type(value) == float and \
           value > 0.0:
            self._tempInc = value
        else:
            raise ValueError('The temperature increment must ' +
                             'be a positive float.')

    @property
    def alphaMin(self):
        if self._alphaMin:
            return self._alphaMin
        else:
            raise RuntimeError('alphaMin has not been defined')

    @alphaMin.setter
    def alphaMin(self, value):
        if type(value) == float and \
           value < 0.0:
            self._alphaMin = value
        else:
            raise ValueError('The minimum alpha must be a negative float.')

    @property
    def alphaMax(self):
        if self._alphaMax:
            return self._alphaMax
        else:
            raise RuntimeError('alphaMax has not been defined')

    @alphaMax.setter
    def alphaMax(self, value):
        if type(value) == float and \
           value > 0.0:
            self._alphaMax = value
        else:
            raise ValueError('The minimum alpha must be a positive float.')

    @property
    def a1(self):
        if self._a1 or self._a1 == 0.0:
            return self._a1
        else:
            raise RuntimeError('a1 has not been defined')

    @a1.setter
    def a1(self, value):
        if type(value) == float:
            self._a1 = value
        else:
            raise ValueError('The a1 must be a float.')

    @property
    def a2(self):
        if self._a2 or self._a2 == 0.0:
            return self._a2
        else:
            raise RuntimeError('a2 has not been defined')

    @a2.setter
    def a2(self, value):
        if type(value) == float:
            self._a2 = value
        else:
            raise ValueError('The a2 must be a float.')

    @property
    def a3(self):
        if self._a3 or self._a3 == 0.0:
            return self._a3
        else:
            raise RuntimeError('a3 has not been defined')

    @a3.setter
    def a3(self, value):
        if type(value) == float:
            self._a3 = value
        else:
            raise ValueError('The a3 must be a float.')

    @property
    def a4(self):
        if self._a4 or self._a4 == 0.0:
            return self._a4
        else:
            raise RuntimeError('a4 has not been defined')

    @a4.setter
    def a4(self, value):
        if type(value) == float:
            self._a4 = value
        else:
            raise ValueError('The a4 must be a float.')

    @property
    def B_z(self):
        if self._B_z or self._B_z == 0.0:
            return self._B_z
        else:
            raise RuntimeError('B_z has not been defined')

    @B_z.setter
    def B_z(self, value):
        if type(value) == float:
            self._B_z = value
        else:
            raise ValueError('The B_z must be a float')

    @property
    def tau(self):
        if self._tau or self._tau == 0.0:
            return self._tau
        else:
            raise RuntimeError('tau has not been defined')

    @B_z.setter
    def tau(self, value):
        if type(value) == float or type(value) == int:
            self._tau = value
        else:
            raise ValueError('tau must be a float or an integer')

    @property
    def dEnergy(self):
        if self._dEnergy:
            return self._dEnergy
        else:
            raise RuntimeError('dEnergy has not been calculated')

    @dEnergy.setter
    def dEnergy(self, value):
        print 'dEnergy is calculated from other given values.'

    def compute_dEnergy(self):
        if self._nEnergy and self._energyMax and self._energyMin:
            self._dEnergy = (self._energyMax - self._energyMin) / self._nEnergy
        else:
            raise RuntimeError('One of the limits has not been defined')

    @property
    def dKPolar(self):
        if self._dKPolar:
            return self._dKPolar
        else:
            raise RuntimeError('dKPolar has not been calculated')

    @dKPolar.setter
    def dKPolar(self, value):
        print 'dKPolar is calculated from other given values'

    def compute_dKPolar(self):
        if self._nKPolar and self._kPolarMax and (self._kPolarMin
                                                  or self.kPolarMin == 0.0):
            self._dKPolar = (self._kPolarMax - self._kPolarMin) / self._nKPolar
        else:
            raise RuntimeError('One of the limits has not been defined')

    @property
    def dKAzimu(self):
        if self._dKAzimu:
            return self._dKAzimu
        else:
            raise RuntimeError('dKAzimu has not been calculated')

    @dKAzimu.setter
    def dKAzimu(self, value):
        print 'dKAzimu is calculated from other given values'

    def compute_dKAzimu(self):
        if self._nKAzimu and self._kAzimuMax and (self._kAzimuMin
                                                  or self._kAzimuMin == 0.0):
            self._dKAzimu = (self._kAzimuMax - self._kAzimuMin) / self._nKAzimu
        else:
            raise RuntimeError('One of the limits has not been defined')

    @property
    def dTemp(self):
        if self._dTemp:
            return self._dTemp
        else:
            raise RuntimeError('dTemp has not been calculated')

    @dTemp.setter
    def dTemp(self, value):
        print 'dTemp is calculated from other given values'

    def compute_dTemp(self):
        if self._nTemp and self._tempMax and (self._tempMin or
                                              self._tempMin == 0.0):
            self._dTemp = (self._tempMax - self._tempMin) / self._nTemp
        else:
            raise RuntimeError('One of the limits has not been defined')

    @property
    def dAlpha(self):
        if self._dAlpha:
            return self._dAlpha
        else:
            raise RuntimeError('dAlpha has not been calculated')

    @dAlpha.setter
    def dAlpha(self, value):
        print 'dAlpha is calculated from other given values'

    def compute_dAlpha(self):
        if self._nAlpha and self._alphaMax and self._alphaMin:
            self._dAlpha = (self._alphaMax - self._alphaMin) / self._nAlpha
        else:
            raise RuntimeError('One of the limits has not been defined')

    @property
    def gamma1(self):
        if self._gamma1:
            return self._gamma1
        else:
            raise RuntimeError('gamma1 has not been calculated')

    @gamma1.setter
    def gamma1(self, value):
        print 'gamma1 is calculated from other given values'

    def compute_gamma1(self):
        if (self._a1 or self._a1 == 0.0) and \
           (self._a4 or self._a4 == 0.0) and \
           self._spinDir:
            if self._spinDir == 'up':
                self._gamma1 = self._a1 - self._a4
            else:
                self._gamma1 = -self._a1 - self._a4
        else:
            raise RuntimeError('One of the limits has not been defined')

    @property
    def gamma2(self):
        if self._gamma2:
            return self._gamma2
        else:
            raise RuntimeError('gamma2 has not been calculated')

    @gamma2.setter
    def gamma2(self, value):
        print 'gamma2 is calculated from other given values'

    def compute_gamma2(self):
        if (self._a2 or self._a2 == 0.0) and \
           (self._a3 or self._a3 == 0.0) and \
           self._spinDir:
            if self._spinDir == 'up':
                self._gamma2 = self._a2 + self._a3
            else:
                self._gamma2 = -self._a2 + self._a3
        else:
            raise RuntimeError('One of the limits has not been defined')


if __name__ == '__main__':

    test = Limits()

    test.spinDir = 'up'
    test.nEnergy = 100
    test.nKPolar = 100
    test.nKAzimu = 100
    test.nTemp = 100
    test.nAlpha = 100
    test.energyMin = -6.0
    test.energyMax = 6.0
    test.kPolarMin = 0.0
    test.kPolarMax = np.pi
    test.kAzimuMin = 0.0
    test.kAzimuMax = 2 * np.pi
    test.T_c = 0.1
    test.tempMin = 0.0
    test.tempMax = 0.1
    test.tempInc = 1.0 / 200.0
    test.alphaMin = -6.0
    test.alphaMax = 6.0
    test.a1 = 0.3
    test.a2 = -0.13
    test.a3 = 0.15
    test.a4 = 0.34
    test.B_z = 1.0

    test.finalise()
    save = test.save()

    test_load = Limits()
    test_load.load(save)
    test_load.finalise()
