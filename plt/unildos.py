import matplotlib.pyplot as plt
import gen.lim as lim
import os

def getFiles():

    return [os.path.join(data_folder, f) for f in os.listdir(data_folder)
            if os.path.isfile(os.path.join(data_folder, f)) and '-0-dos' in f]
L = lim.Limits()
L..readData(getFiles()[0])
