'''
    min: f(x)
     st. Eq_A' x  = Eq_b
         In_A' x >= In_b
'''
import sys
import numpy as np
import inspect
from .problem_ import Problem

class NLP(Problem):
    def __init__(self, f, dim, **kwargs ):

        # Setup the class fields
        self.type   = 'NLP'
        self.f      = f
        self.dim    = dim

        Problem.__init__(self, **kwargs)
        Problem._check_class(self)

    # =========================================================================
    def set_field(self, f=[],dim=[],**kwargs):

        if f    != []: self.f   = f
        if dim  != []: self.dim = dim
        Problem.set_field(self,**kwargs)
        Problem._check_class(self)

    # =========================================================================
    # Utility
    def print(self):
        string = (
            'This is a Non Linear program on the form,'  +
            __doc__ + '\n' +
            'Variables are defined by,\n'
            'f:\n' + inspect.getsource(self.f)
        )
        
        string += Problem.print(self)
        print(string)
        
    def help(self):
        print('Class of Quadratic programs on the form,')
        print(__doc__ + Problem.help(self))