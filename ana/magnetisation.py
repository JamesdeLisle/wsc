import numpy as np
import gen.parser as ps
from gen.lim import Limits
import kel.par as par
import gen.forms as fm
import sys
from uti import simpFactor


class MAG:

    def __init__(self, path, order):

        self.path = path
        self.lim = Limits()
        self.spin = ['up', 'dn']
        self.lim.readData(self.path)
        if order == '1':
            self.orders = ['1']
        elif order == '3':
            self.orders = ['1', '3']
        elif order == '4':
            self.orders = ['1', '3', '4']
        elif order == '5':
            self.orders = ['1', '3', '4', '5']
        else:
            print '%s is not a valid order to compute.' % order
            sys.exit()
        self.P = {}
        for order in self.orders:
            self.P[order] = {'up': par.ParamSpace(self.lim, order, 'gK'),
                             'dn': par.ParamSpace(self.lim, order, 'gK')}

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
                    g = np.zeros(shape=(2, 2), dtype=np.complex128)
                    for order in self.orders:
                        g += self.P[order]['up'].data['gK'][iXi, iTheta]
                        g -= self.P[order]['dn'].data['gK'][iXi, iTheta]
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
