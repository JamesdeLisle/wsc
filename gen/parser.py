from os import listdir
from os.path import join, isfile
from jsci.Coding import NumericDecoder
import json


def nameParser(filename, part):
    if part == 'run':
        return filename[-27:-13]
    elif part == 'run+order':
        return filename[-27:-10]
    elif part == 'run+order+temp':
        return filename[-27:-5]
    elif part == 'temp':
        return filename[-9:-5]


def filter(order, folder, kind):
    if kind == 'raw':
        return [join(folder, f) for f in listdir(folder)
                if isfile(join(folder, f))
                and '-%s-' % (order) in f
                and 'dos' not in f]
    if kind == 'dos':
        return [join(folder, f) for f in listdir(folder)
                if isfile(join(folder, f))
                and '-%s-' % (order) in f
                and 'dos' in f]


def getFiles(orders, folder, kind):
    return {order: sorted(filter(order, folder, kind)) for order in orders}


def getData(files):
    rv = {}
    for f in files:
        rv[f] = json.loads(f.read(), cls=NumericDecoder)['data']
    return rv
