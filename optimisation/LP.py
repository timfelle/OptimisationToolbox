'''
    min: g' x,
     st. Eq_A' x  = Eq_b,
         In_A' x >= In_b.
'''
import sys
import numpy as np
from ._problem import Problem

class LP(Problem):
    def __init__(self, g, **kwargs):

        # Setup the class fields
        self.type   = 'LP'
        self.dim    = g.shape[0]
        self.g      = g
        
        Problem.__init__(self, **kwargs)
        self._check_class()

    def f(self,x):
        x = np.matrix( x ).T
        return self.g.T * x

    # =========================================================================
    def set_field(self, g=[], **kwargs):

        if g    != []: self.g = g
        Problem.set_field(self, **kwargs)

        self.dim    = self.g.shape[0]
        self._check_class()

    # =========================================================================
    def _check_class(self):

        # _____________________________________________________________________
        # Check for Errors
        err = ''

        if self.g.shape[0] != self.dim:
            err+= 'File "LP.py", input error\n'
            err+= '  g must be of shape (%d,1).\n' % self.dim

        if err != '':
            print( err ,file=sys.stderr)
            exit()
        
        Problem._check_class(self)
    
    # =========================================================================
    # Utility

    def print(self):
        g_string = ''
        
        # Setup the g vector
        for g_i in self.g: 
            g_string += '   %5.2f \n' % g_i
            
        string = (
            'This is a Linear program on the form,' +
            __doc__ + '\n' +
            'Variables are defined by,\n'
            'g:\n' + g_string
        )
        
        string += Problem.print(self)
        print(string)
    
    def help(self):
        print('Class of Linear programs on the form,')
        print(__doc__ + Problem.help(self))