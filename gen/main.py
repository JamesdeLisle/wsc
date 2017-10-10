from multiprocessing import Pool
import itertools
import os


def worker(runValue):

    if runValue.order == '0':
        import uni.unifunc as func
    elif runValue.order == '1':
        import ret.retfunc as func
    elif runValue.order == '2':
        import kel.RK as func

    F = func.Function(runValue)

    return {'index': runValue.index,
            'value': getattr(F, runValue.string)}


class Main:

    def __init__(self, limits, start_time, data_folder, order):

        self.limits = limits
        self.start_time = start_time
        self.data_folder = data_folder
        self.order = order

        if order in ['0', '1', '2', '3']:
            self.order = order
        else:
            raise ValueError("The given order is not valid")

        if self.order == '0':
            import uni.uniparam as param
            # self.strings = ['gR', 'gK']
            self.strings = ['gR']
        elif self.order == '1':
            import ret.retparam as param
            self.strings = ['gR1']
        elif self.order == '2':
            import kel.kelparam as param
            self.strings = ['gK1']

        self.P = param.ParamSpace(self.limits, self.order, self.strings)
        self.DOF = itertools.product(enumerate(self.P.temp),
                                     enumerate(self.P.ener))

    def run(self):

        print('Calculating order %s...' % self.order)

        for (iT, T), (iE, E) in self.DOF:
            self.P.getProgress(iT, iE)
            self.P.initData((iT, iE))
            self.P.loadData(self.data_folder,
                            self.start_time,
                            iT,
                            iE)
            self.DATA = {}

            ######################################
            if True:
                runs = self.P.getRun(iT, iE, self.strings[0])
                for run in runs:
                    worker(run)
            ######################################

            for string in self.strings:
                run = self.P.getRun(iT, iE, string)
                p = Pool()
                self.DATA[string] = p.map(worker, run)
                p.close()

            for string in self.strings:
                self.P.updateData(self.DATA[string], string)

            del self.DATA

            self.P.writeData(os.path.join(self.data_folder, self.start_time))
