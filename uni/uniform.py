import uniparam
import unifunc
from multiprocessing import Pool
import itertools


def worker(runValue):

    U = unifunc.Uniform(runValue)

    return {'index': runValue.index,
            'value': U[runValue.string]}


class UniformMain:

    def __init__(self, limits, start_time, data_folder):

        self.start_time = start_time
        self.data_folder = data_folder
        self.limits = limits

    def run(self):

        P = uniparam.ParamSpace(self.limits)

        for (iT, T), (iE, E) in itertools.product(enumerate(P.temp),
                                                  enumerate(P.energy)):

            P.initialiseData((iT, iE))
            strings = ['g_RET', 'g_KEL']
            DATA = dict()

            ######################################
            # runs = P.getRun( iT, iE, trings[0] )
            # for run in runs:
            #     X = worker( run )
            ######################################

            for string in strings:
                print 'computing %s...' % (string)
                run = P.getRun(iT, iE, string)
                p = Pool()
                DATA[string] = p.map(worker, run)
                p.close()

            for string in strings:
                P.updateData(DATA[string], string)

            del DATA

            P.writeData('%s%s' % (self.data_folder, self.start_time))
            print '#######--%d-%d--#######' % (iT, iE)

        print 'Done!'
