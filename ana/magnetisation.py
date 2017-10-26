import numpy as np
import gen.parser as ps
from gen.lim import Limits
import kel.par as kPar
import urt.par as uPar
import gen.forms as fm
import sys
from uti import simpFactor


class MAG:

    def __init__(self, path, zero=False):

        self.path = path
        self.lim = Limits()
        self.zero = zero
        self.spin = ['up', 'dn']
        self.lim.readData(self.path)
        self.P = {}
        self.P['1'] = {'up': uPar.ParamSpace(self.lim, '1', 'gK'),
                       'dn': uPar.ParamSpace(self.lim, '1', 'gK')}
        self.P['3'] = {'up': kPar.ParamSpace(self.lim, '3', 'gK'),
                       'dn': kPar.ParamSpace(self.lim, '3', 'gK')}

    def compute(self):

        print 'Calculating magnetisation...'
        rv = 0.0
        for iE, E in enumerate(self.P['1']['up'].ener):
            hE = 0.0
            sys.stdout.write('\r%.2f%%' % (100 * iE / (self.lim.nEnergy - 1)))
            sys.stdout.flush()
            for order in self.P:
                for spin in self.spin:
                    f = ps.getFile(self.path, order, spin, iE)
                    self.P[order][spin].readData(f[iE])
            for iXi, Xi in enumerate(self.P['1']['up'].kPol):
                hXi = 0.0
                for iTheta, Theta in enumerate(self.P['1']['up'].kAzi):
                    hTheta = 0.0
                    if self.zero:
                        g = self.P['1']['up'].data['gK'][iXi, iTheta] \
                            - self.P['1']['dn'].data['gK'][iXi, iTheta]
                    else:
                        g = self.P['1']['up'].data['gK'][iXi, iTheta] \
                            + self.P['3']['up'].data['gK'][iXi, iTheta] \
                            - self.P['1']['dn'].data['gK'][iXi, iTheta] \
                            - self.P['3']['dn'].data['gK'][iXi, iTheta]
                    hTheta += np.trace(np.dot(fm.p3(), g))
                    hTheta /= 8 * np.pi * np.pi
                    hTheta *= self.lim.dKAzimu
                    hTheta *= simpFactor(iTheta, self.lim.nKAzimu)
                    hXi += hTheta
                hXi *= np.sin(Xi) * self.lim.dKPolar * 3.0 / 8.0
                hXi *= simpFactor(iXi, self.lim.nKPolar)
                hE += hXi
            hE *= self.lim.dEnergy * 3.0 / 8.0
            hE *= simpFactor(iE, self.lim.nEnergy)
            rv += hE
        print '\nDone!'
        return np.imag(rv)
