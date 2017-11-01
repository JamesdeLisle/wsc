import numpy as np
import gen.parser as ps
from gen.lim import Limits
import kel.par as kPar
import urt.par as uPar
import gen.forms as fm
import sys
from uti import simpFactor


class HCOND:

    def __init__(self, path, spin):

        self.path = path
        self.spin = spin
        self.lim = Limits()
        self.lim.readData(self.path)
        self.P = {}
        self.P['1'] = uPar.ParamSpace(self.lim, '1', 'gK')
        self.P['3'] = kPar.ParamSpace(self.lim, '3', 'gK')
        self.P['4'] = kPar.ParamSpace(self.lim, '4', 'gK')
        self.P['5'] = kPar.ParamSpace(self.lim, '5', 'gK')

    def compute(self):

        print 'Calculating heat current...'
        rv = 0.0
        for iE, E in enumerate(self.P['1'].ener):
            hE = 0.0
            sys.stdout.write('\r%.2f%%' % (100 * iE / (self.lim.nEnergy - 1)))
            sys.stdout.flush()
            for order in self.P:
                f = ps.getFile(self.path, order, self.spin, iE)
                self.P[order].readData(f[iE])
            for iXi, Xi in enumerate(self.P['1'].kPol):
                hXi = 0.0
                for iTheta, Theta in enumerate(self.P['1'].kAzi):
                    hTheta = 0.0
                    g = np.zeros(shape=(2, 2), dtype=np.complex128)
                    for order in self.P:
                        g += self.P[order].data['gK'][iXi, iTheta]
                    hTheta += np.trace(np.dot(fm.p3(), g))
                    hTheta /= 8 * np.pi * np.pi
                    hTheta *= self.lim.dKAzimu
                    hTheta *= simpFactor(iTheta, self.lim.nKAzimu)
                    hXi += hTheta
                hXi *= np.sin(Xi) * np.cos(Xi) * self.lim.dKPolar * 3.0 / 8.0
                hXi *= simpFactor(iXi, self.lim.nKPolar)
                hE += hXi
            hE *= E * self.lim.dEnergy * 3.0 / 8.0
            hE *= simpFactor(iE, self.lim.nEnergy)
            rv += hE
        print '\nDone!'
        return np.imag(rv)
