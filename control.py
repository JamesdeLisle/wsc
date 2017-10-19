import main
import analysis
from gen.parser import getFiles
import os


shift = 0.005
data_folder = 'data/'
store_folder = 'store/'

orders = ['0', '1']
for i in range(100):
    main.Main(i * shift)
    analysis.Main()
    fs = getFiles(orders, data_folder, 'raw')
    for order, lst in fs.iteritems():
        for f in lst:
            os.remove(f)
