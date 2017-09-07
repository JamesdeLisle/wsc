import retfunc
import retparam
from multiprocessing import Pool
import itertools
import os


def worker(runValue):

    U = retfunc.Retarded(runValue)

    return {'index': runValue.index,
            'value': getattr(U, runValue.string)}


class RetardedMain:

    def __init__(self, limits, start_time, data_folder):

        self.limits = limits
        self.start_time = start_time
        self.data_folder = data_folder
        self.order = '1'
        self.strings = ['gR1']

    def run(self):

        P = retparam.ParamSpace(self.limits, self.order, self.strings)

        print('Calculating first order Retarded...')
        for (iT, T), (iE, E) in itertools.product(enumerate(P.temp),
                                                  enumerate(P.ener)):

            P.getProgress(iT, iE)
            P.initData((iT, iE))
            f = os.path.join(self.data_folder,
                             self.start_time +
                             '-0-T%03dE%03d' % (iT, iE))
            P.loadData(f)
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

        print ('\nDone!')
