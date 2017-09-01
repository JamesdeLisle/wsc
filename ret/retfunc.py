import gen.env as env
import numpy as np


class Retarded:

    def __init__(self, value_set, dG0):

        self.value_set = value_set
        self.environment = env.Environment(value_set)
        self.dG0 = dG0
        self.store = dict()

    def g_RET_FUNC(self, G_IN):

        VAL = self.value_set
        ENV = self.environment

        epsilon = np.zeros(shape=(2, 2))
        epsilon[0, 0] = VAL['energy']
        epsilon[1, 1] = -VAL['energy']

        # print epsilon
        # print ENV[ 'HAM_R' ]
        # print G_IN
        # print self.commute( epsilon - ENV[ 'HAM_R' ], G_IN )

        return self.dG0 + self.commute(epsilon - ENV['HAM_R'], G_IN)

    def commute(self, A, B):

        return np.dot(A, B) - np.dot(B, A)
