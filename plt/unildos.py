import matplotlib.pyplot as plt
import gen.lim as lim
import os
import uni.uniparam as par
from jsci.Coding import NumericDecoder
import json

def getFiles(data_folder):

    return [os.path.join(data_folder, f) for f in os.listdir(data_folder)
            if os.path.isfile(os.path.join(data_folder, f))]


data_folder = 'datacal/'
files = sorted(getFiles(data_folder))
data = []
for f in files:
    with open(f, 'r') as F:
        content = json.loads(F.read(), cls=NumericDecoder)
    data.append(content['data'])

for x in data:

    plt.plot(x)

plt.show()
