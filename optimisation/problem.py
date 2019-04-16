'''
The following functions have been defined for the class.
- set_field:        Redefines any of the problem or constraint parameters.
- add_constraint:   Add additional equality or inequality constraints.
- print:            Print the full definition of the program currently in use.
- display:          Plots the problem, only 2D.
- help:             Print this message.
'''
import sys
import numpy as np
from .display import display as disp
from .solver import solver
import inspect

class Problem:
    def __init__(self,
        Eq_A=[], Eq_b=[],
        In_A=[], In_b=[],
        Eq_C=[], In_C=[]
        ):
        
        if not isinstance(Eq_A, np.matrix): Eq_A = np.matrix(Eq_A).T
        if not isinstance(Eq_b, np.matrix): Eq_b = np.matrix(Eq_b).T
        if not isinstance(In_A, np.matrix): In_A = np.matrix(In_A).T
        if not isinstance(In_b, np.matrix): In_b = np.matrix(In_b).T
        if not isinstance(Eq_C, list)     : Eq_C = [Eq_C]
        if not isinstance(In_C, list)     : In_C = [In_C]
        
        # Setup the class fields 
        self.Eq_A   = Eq_A
        self.Eq_b   = Eq_b
        self.In_A   = In_A
        self.In_b   = In_b
        self.Eq_C   = Eq_C
        self.In_C   = In_C

        self.dim = None
        self.type   = ''
        self.x_opt  = []
        self.f_opt  = []
        self.x_list = []


    # =========================================================================
    def set_field(self, Eq_A=[], Eq_b=[], In_A=[], In_b=[], Eq_C=[], In_C=[]):

        if not isinstance(Eq_A, np.matrix): Eq_A = np.matrix(Eq_A).T
        if not isinstance(Eq_b, np.matrix): Eq_b = np.matrix(Eq_b).T
        if not isinstance(In_A, np.matrix): In_A = np.matrix(In_A).T
        if not isinstance(In_b, np.matrix): In_b = np.matrix(In_b).T
        if not isinstance(Eq_C, list)     : Eq_C = [Eq_C]
        if not isinstance(In_C, list)     : In_C = [In_C]
        
        if Eq_A.size: self.Eq_A = Eq_A
        if Eq_b.size: self.Eq_b = Eq_b
        if In_A.size: self.In_A = In_A
        if In_b.size: self.In_b = In_b
        if Eq_C.size: self.Eq_C = Eq_C
        if In_C.size: self.In_C = In_C

        self._check_class()

    def add_constraints(self,Eq_A=[],Eq_b=[],In_A=[],In_b=[],Eq_C=[],In_C=[]):
        # Addition of constraints to the system.

        if not isinstance(Eq_A, np.matrix): Eq_A = np.matrix(Eq_A).T
        if not isinstance(Eq_b, np.matrix): Eq_b = np.matrix(Eq_b).T
        if not isinstance(In_A, np.matrix): In_A = np.matrix(In_A).T
        if not isinstance(In_b, np.matrix): In_b = np.matrix(In_b).T
        if not isinstance(Eq_C, list)     : Eq_C = [Eq_C]
        if not isinstance(In_C, list)     : In_C = [In_C]

        # _____________________________________________________________________
        # Ensure inputs match the necessary sizes.
        if ( Eq_A.size != 0 and Eq_A.shape[0] != self.dim ):
            print('Error in add_constraints',file=sys.stderr)
            print('  Eq_A must comply with problem dimension. Eq_A: %d, Dim: %d' 
                %(Eq_A.shape[0], self.dim),
                file=sys.stderr)
            exit()

        if ( In_A.size != 0 and In_A.shape[0] != self.dim ):
            print('Error in add_constraints',file=sys.stderr)
            print('  In_A must comply with problem dimension. In_A: %d, Dim: %d' 
                %(In_A.shape[0],self.dim),
                file=sys.stderr)
            exit()

        if Eq_A.size != 0 and Eq_A.shape[1] != len(Eq_b):
            print('Error in add_constraints',file=sys.stderr)
            print('  Eq_A and Eq_b must match.',file=sys.stderr)
            exit()

        if In_A.size != 0 and In_A.shape[1] != len(In_b):
            print('Error in add_constraints',file=sys.stderr)
            print('  In_A and In_b must match.',file=sys.stderr)
            exit()

        # _____________________________________________________________________
        # Place constraints in the data structure
        
        if self.Eq_A.size == 0 and Eq_A.size != 0:
            self.set_field(Eq_A=Eq_A,Eq_b=Eq_b)
        elif Eq_A.size != 0:
            self.Eq_A = np.hstack([ self.Eq_A,Eq_A ])
            self.Eq_b = np.vstack([ self.Eq_b,Eq_b ])
        
        if self.In_A.size == 0 and In_A.size != 0:
            self.set_field(In_A=In_A,In_b=In_b)
        elif In_A.size != 0:
            self.In_A = np.hstack([ self.In_A,In_A ])
            self.In_b = np.vstack([ self.In_b,In_b ])
        
        if self.Eq_C.size == 0 and Eq_C.size != 0:
            self.set_field(Eq_C=Eq_C)
        elif In_C != 0:
            self.In_C.append(In_C)

        if self.In_C.size == 0 and In_C.size != 0:
            self.set_field(In_C=In_C)
        elif In_C != 0:
            self.In_C.append(In_C)

        # Make sure no errors have occured
        self._check_class()

    # =========================================================================
    def solve(self):
        x_opt, f_opt = solver(self)
        self.x_opt = x_opt
        self.f_opt = f_opt
        
    # =========================================================================
    def _check_class(self):
        err = ''
        # _____________________________________________________________________
        # Check for Errors

        if self.Eq_A.shape[0] != self.dim and self.Eq_A.size != 0:
            err+= 'File, input error\n'
            err+= '  Eq_A must be of shape (%d,N).\n' % self.dim

        if self.Eq_b.shape[0] != self.Eq_A.shape[1] and self.Eq_b.size != 0:
            err+= 'File, input error\n'
            err+= '  Eq_b must match Eq_A, (%d,1).\n' % self.Eq_A.shape[1]

        if self.In_A.shape[0] != self.dim and self.In_A.size != 0:
            err+= 'File, input error\n'
            err+= '  In_A must be of shape (%d,N).\n' % self.dim

        if self.In_b.shape[0] != self.In_A.shape[1] and self.In_b.size != 0:
            err+= 'File, input error\n'
            err+= '  In_b must match In_A, (%d,1).\n' % self.In_A.shape[1]

        if err != '':
            print( err ,file=sys.stderr)
            exit()

    # =========================================================================
    # Utility

    def print(self):

        N_eq_L = len(self.Eq_b)
        N_in_L = len(self.In_b)
        N_eq_N = len(self.Eq_C)
        N_in_N = len(self.In_C)

        string = ''
        
        # Setup string for Equality A
        Eq_A_string = ''
        for i in range(0,self.Eq_A.shape[0]):
            Eq_A_string += '   '
            for j in range(0,self.Eq_A.shape[1]):
                Eq_A_string += '%5.2f ' % self.Eq_A[i,j]
            if i != self.Eq_A.shape[0]:
                Eq_A_string += '\n'
        
        # Setup the Eq_b vector
        Eq_b_string = ''
        for i in range(0,self.Eq_b.shape[0]):
            Eq_b_string += '   %5.2f \n' % self.Eq_b[i]

        # Setup the In_A matrix
        In_A_string = ''
        for i in range(0,self.In_A.shape[0]):
            In_A_string += '   '
            for j in range(0,self.In_A.shape[1]):
                In_A_string += '%5.2f ' % self.In_A[i,j]
            if i != self.In_A.shape[0]:
                In_A_string += '\n'
        
        # Setup the In_b vector
        In_b_string = ''
        for i in range(0,N_in_L):
            In_b_string += '   %5.2f \n' % self.In_b[i]
        

        # Setup the non linear equality constraints
        Eq_C_string = ''
        if N_eq_N:
            tmp = inspect.getsource(self.Eq_C[1])
            Eq_C_string += tmp


        # Setup the non linear inequality constraints
        In_C_string = ''
        if N_in_N:
            In_C_string += inspect.getsource(self.In_C[0])

        # Solution string
        Sol_str = ''
        if len(self.x_opt) > 0:
            Sol_str = '\nSolution with value %.2f ' % self.f_opt
            Sol_str += 'have been found at the point:\n'
            for x in self.x_opt:
                Sol_str += '   %5.2f\n' % x

        
        string += '\nAnd constraints defined by,\n'
        if N_eq_L: string += 'Eq_A:\n' + Eq_A_string
        if N_eq_L: string += 'Eq_b:\n' + Eq_b_string
        if N_in_L: string += 'In_A:\n' + In_A_string
        if N_in_L: string += 'In_b:\n' + In_b_string
        if N_eq_N: string += 'Eq_C:\n' + Eq_C_string
        if N_in_N: string += 'In_C:\n' + In_C_string
        string += Sol_str
        return string
        
    def display(self, **kwargs):
        return disp(self, **kwargs)

    def help(self):
        return __doc__