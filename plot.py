import plt.dosline as lin
import os
from gen.parser import getFiles


def plotSingle():
    data_folder = os.path.join(os.getcwd(), 'data/')

    orders = ['0', '2', 'total']
    files = getFiles(orders, data_folder, 'dos')

    for order in orders:
        lin.dosline(files[order][0], order)


if __name__ == '__main__':
    print 'Plotting...'
    plotSingle()
    print 'Done!'
