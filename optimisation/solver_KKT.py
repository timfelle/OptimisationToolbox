'''
KKT Based QP solver
'''

import sys
from .problem_ import Problem

class solver_KKT:
    def __init__(self,problem):
        if not isinstance(problem,Problem) or problem.type != 'QP':
            print('Only QP\'s are supported',file=sys.stderr)
            exit()

        self.kkt = []

