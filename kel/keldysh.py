import RK
import kelparam
from multiprocessing import Pool
import itertools
import os


def worker(runValue):

    U = RK.RK(runValue)

    return {'index': runValue.index,
            'value': getattr(U, runValue.string)}


class KeldyshMain:

    def __init__(self, limits, start_time, data_folder):

        self.limits = limits
        self.start_time = start_time
        self.data_folder = data_folder
        self.order = '2'
        self.strings = ['gK1']

    def run(self):

        P = kelparam.ParamSpace(self.limits, self.order, self.strings)

        print 'Calculating first order Keldysh...'
        for (iT, T), (iE, E) in itertools.product(enumerate(P.temp),
                                                  enumerate(P.ener)):

            P.getProgress(iT, iE)
            P.initData((iT, iE))
            f_g0 = os.path.join(self.data_folder,
                                self.start_time +
                                '-0-T%03dE%03d' % (iT, iE))
            f_gR = os.path.join(self.data_folder,
                                self.start_time +
                                '-1-T%03dE%03d' % (iT, iE))
            P.loadData(f_g0, f_gR)
            DATA = dict()

            ######################################
            if False:
                runs = P.getRun(iT, iE, self.strings[0])
                for run in runs:
                    worker(run)
            #####################################

            for string in self.strings:
                run = P.getRun(iT, iE, string)
                p = Pool()
                DATA[string] = p.map(worker, run)
                p.close()

            for string in self.strings:
                P.updateData(DATA[string], string)

            del DATA

            P.writeData(os.path.join(self.data_folder, self.start_time))

        print '\nDone!'
