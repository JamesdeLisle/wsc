from os import listdir
from os.path import join, isfile
from jsci.Coding import NumericDecoder
import json


def fileName(order, spinDir, iT, iE):
    return '-%s-%s-T%04dE%04d' % (order, spinDir, iT, iE)


def nameParser(filename, part):
    if part == 'run':
        return filename[-30:-16]
    elif part == 'run+order':
        return filename[-30:-13]
    elif part == 'run+order+spin':
        return filename[-30:-10]
    elif part == 'run+order+spin+temp':
        return filename[-30:-5]
    elif part == 'temp':
        return filename[-10:-5]
    elif part == 'spin+temp':
        return filename[-14:-5]


def filter(order, spin, folder, kind):
    if kind == 'raw':
        return [join(folder, f) for f in listdir(folder)
                if isfile(join(folder, f))
                and '-%s-' % (spin) in f
                and '-%s-' % (order) in f
                and 'dos' not in f]
    if kind == 'dos':
        return [join(folder, f) for f in listdir(folder)
                if isfile(join(folder, f))
                and '-%s-' % (spin) in f
                and '-%s-' % (order) in f
                and 'dos' in f]
    if kind == 'lims':
        return [join(folder, f) for f in listdir(folder)
                if isfile(join(folder, f))
                and 'lims' in f]


def getFile(folder, order, spin, iE):
    return sorted(filter(order, spin, folder, 'raw'))


def getLims(path):
    return filter('0', 'up', path, 'lims')[0]


def getFiles(orders, spin, folder, kind):
    return {order: sorted(filter(order, spin, folder, kind)) for order in orders}


def getData(path):
    with open(path, 'r') as f:
        return json.loads(f.read(), cls=NumericDecoder)['data']
