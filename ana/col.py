import numpy as np
import gen.par as par
import gen.lim as lim
import os


class Collate:

    def __init__(self, data_folder):

        self.data_folder = data_folder
        files = [f for f in os.listdir(data_folder)
                 if os.path.isfile(os.path.join(data_folder, f))]

        if not files:
            raise IOError("No data files exist!")

        files = {}
        sets = ['0', '1', '2']
        for s in sets:
            files[s] = [f for f in files if '-%s-' % (s) in f]

        self.run_time = files['0'][0][0:13]

        L = lim.Limits()
        P = par.ParamSpaceBase(
