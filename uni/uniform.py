import uniparam
import unifunc
from multiprocessing import Pool
import itertools
import os


def worker(runValue):

    runValue.compSpace()
    U = unifunc.Uniform(runValue)

    return {'index': runValue.index,
            'value': getattr(U, runValue.string)}


class UniformMain:

    def __init__(self, limits, start_time, data_folder):

        self.limits = limits
        self.start_time = start_time
        self.data_folder = data_folder
        self.order = '0'
        self.strings = ['gR', 'gK']

    def run(self):

        P = uniparam.ParamSpace(self.limits, self.order, self.strings)

        for (iT, T), (iE, E) in itertools.product(enumerate(P.temp),
                                                  enumerate(P.ener)):

            P.initData((iT, iE))
            DATA = dict()

            ######################################
            #runs = P.getRun(iT, iE, self.strings[1])
            #for run in runs:
            #    
            #    X = worker(run)
            ######################################

            for string in self.strings:
                print 'computing %s...' % (string)
                run = P.getRun(iT, iE, string)
                p = Pool()
                DATA[string] = p.map(worker, run)
                p.close()

            for string in self.strings:
                P.updateData(DATA[string], string)

            del DATA

            P.writeData(os.path.join(self.data_folder, self.start_time))
            print '#######--%d-%d--#######' % (iT, iE)

        print 'Done!'
