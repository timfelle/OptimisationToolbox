'''
    min: x' H x + g' x,
     st. Eq_A' x  = Eq_b,
         In_A' x >= In_b,
         In_C(x) >= 0.
'''
import sys
import numpy as np
from .problem import Problem

class QP(Problem):
    def __init__(self, H, g=[], **kwargs):
        Problem.__init__(self, **kwargs)
        if g == []: g = np.matrix(np.zeros(H.shape[0])).T
        
        # Setup the class fields
        self.type   = 'QP'
        self.dim    = H.shape[0]
        self.H      = H
        self.g      = g
        
        self._check_class()

    def f(self,x):
        if not isinstance(x, np.matrix): x = np.matrix( x ).T
        return 0.5*x.T*self.H*x + self.g.T * x

    def Df(self,x):
        if not isinstance(x, np.matrix): x = np.matrix( x ).T
        return self.H*x + self.g

    # =========================================================================
    def set_field(self, H=[], g=[], **kwargs):

        if H    != []: self.H = H
        if g    != []: self.g = g
        Problem.set_field(self, **kwargs)

        self.dim    = self.H.shape[0]
        self._check_class()

    # =========================================================================
    def _check_class(self):

        # Examine definiteness of H
        sym = np.allclose(self.H, self.H.T, atol=1e-8)
        eig = np.linalg.eigvals(self.H)
        if      min(eig) >= 0: definite = 'Positive'
        elif    max(eig) <= 0: definite = 'Negative'
        else                 : definite = 'In'

        if ('In' not in definite) and (0 in eig): definite += 'Semi'
        definite += 'Definite'
        self.definite = definite

        # _____________________________________________________________________
        # Check for Errors
        err = ''

        if self.H.shape[0] != self.H.shape[1] or not sym:
            err+= 'File "QP.py", input error\n'
            err+= '  H must be symetric and square.\n'

        if self.g.shape[0] != self.dim:
            err+= 'File "QP.py", input error\n'
            err+= '  g must be of shape (%d,1).\n' % self.dim

        if err != '':
            print( err ,file=sys.stderr)
            exit()
        
        Problem._check_class(self)
    
    # =========================================================================
    # Utility

    def print(self):
        H_string = g_string = ''

        # Setup the H matrix
        for i in range(self.H.shape[0]):
            H_string += '   '
            for j in range(self.H.shape[1]):
                H_string += '%5.2f ' % self.H[i,j]
            if i != self.H.shape[0]:
                H_string += '\n'
        
        # Setup the g vector
        for g_i in self.g: 
            g_string += '   %5.2f \n' % g_i
            
        string = (
            'This is a symmetric %s Quadratic program on the form,' 
            % self.definite + 
            __doc__ + '\n' +
            'Variables are defined by,\n'
            'H:\n' + H_string + 'g:\n' + g_string
        )
        
        string += Problem.print(self)
        print(string)
    
    def help(self):
        print('Class of Quadratic programs on the form,')
        print(__doc__ + Problem.help(self))