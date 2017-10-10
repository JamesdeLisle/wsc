import numpy as np


def p0():

    return np.eye(2, dtype=np.complex128)


def p1():

    rv = np.zeros(2, dtype=np.complex128)
    rv[1, 0] = 1.0
    rv[0, 1] = 1.0
    return rv


def p2():

    rv = np.zeros(2, dtype=np.complex128)
    rv[0, 1] = -1.0 * 1j
    rv[1, 0] = 1.0 * 1j
    return rv


def p3():

    rv = np.eye(2, dtype=np.complex128)
    rv[1, 1] = -rv[1, 1]
    return rv
