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

class Problem:
    def __init__(self,
        In_A=[], In_b=[],
        Eq_A=[], Eq_b=[]
        ):

        if In_A == []:  In_A = np.matrix(In_A).T
        if In_b == []:  In_b = np.matrix(In_b).T
        if Eq_A == []:  Eq_A = np.matrix(Eq_A).T
        if Eq_b == []:  Eq_b = np.matrix(Eq_b).T

        # Setup the class fields
        self.In_A   = In_A
        self.In_b   = In_b 
        self.Eq_A   = Eq_A
        self.Eq_b   = Eq_b
        if self.dim == []: self.dim = 0

    # =========================================================================
    def set_field(self,In_A=[], In_b=[], Eq_A=[], Eq_b=[]):

        if In_A != []: self.In_A = In_A
        if In_b != []: self.In_b = In_b
        if Eq_A != []: self.Eq_A = Eq_A
        if Eq_b != []: self.Eq_b = Eq_b

        self._check_class()

    def add_constraints(self,In_A=[],In_b=[],Eq_A=[],Eq_b=[]):
        # Addition of constraints to the system.


        In_A = np.matrix(In_A).T
        In_b = np.matrix(In_b).T
        Eq_A = np.matrix(Eq_A).T
        Eq_b = np.matrix(Eq_b).T

        if self.Eq_A.size == 0 and Eq_A.size != 0:
            self.set_field(Eq_A=Eq_A,Eq_b=Eq_b)
        if self.In_A.size == 0 and In_A.size != 0:
            self.set_field(In_A=In_A,In_b=In_b)
        

        if ( In_A.size != 0 and In_A.shape[0] != self.dim ):
            print('Error in add_constraints',file=sys.stderr)
            print('  In_A must comply with problem dimension. In_A: %d, Dim: %d' 
                %(In_A.shape[0],self.dim),
                file=sys.stderr)
            exit()

        if ( Eq_A.size != 0 and Eq_A.shape[0] != self.dim ):
            print('Error in add_constraints',file=sys.stderr)
            print('  Eq_A must comply with problem dimension. Eq_A: %d, Dim: %d' 
                %(Eq_A.shape[0], self.dim),
                file=sys.stderr)
            exit()

        # Add inequality
        if In_A.size != 0 and In_A.shape[1] != len(In_b):
            print('Error in add_constraints',file=sys.stderr)
            print('  In_A and In_b must match.',file=sys.stderr)
            exit()
        elif In_A.size != 0: 
            self.In_A = np.hstack([ self.In_A,In_A ])
            self.In_b = np.vstack([ self.In_b,In_b ])
        
        if Eq_A.size != 0 and Eq_A.shape[1] != len(Eq_b):
            print('Error in add_constraints',file=sys.stderr)
            print('  Eq_A and Eq_b must match.',file=sys.stderr)
            exit()
        elif Eq_A.size != 0:
            self.Eq_A = np.hstack([ self.Eq_A,Eq_A ])
            self.Eq_b = np.vstack([ self.Eq_b,Eq_b ])

        self._check_class()

    # =========================================================================
    def _check_class(self):
        err = ''
        # _____________________________________________________________________
        # Check for Errors

        if self.In_A.size != 0 and self.In_A.shape[0] != self.dim:
            err+= 'File, input error\n'
            err+= '  In_A must be of shape (%d,N).\n' % self.dim

        if self.In_b.size != 0 and (self.In_b.shape[0] != self.In_A.shape[1]):
            err+= 'File, input error\n'
            err+= '  In_b must match Eq_A, (%d,1).\n' % self.In_A.shape[1]
                
        if self.Eq_A.size != 0 and self.Eq_A.shape[0] != self.dim:
            err+= 'File, input error\n'
            err+= '  Eq_A must be of shape (%d,N).\n' % self.dim

        if self.Eq_b.size != 0 and (self.Eq_b.shape[0] != self.Eq_A.shape[1]):
            err+= 'File, input error\n'
            err+= '  Eq_b must match Eq_A, (%d,1).\n' % self.Eq_A.shape[1]

        if err != '':
            print( err ,file=sys.stderr)
            exit()

    # =========================================================================
    # Utility

    def print(self):
        string = ''
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
        for i in range(0,self.In_b.shape[0]):
            In_b_string += '   %5.2f \n' % self.In_b[i]
        
        # Setup the H matrix
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
        
        string += '\nAnd constraints defined by,\n'
        string += 'Eq_A:\n' + Eq_A_string
        string += 'Eq_b:\n' + Eq_b_string
        string += 'In_A:\n' + In_A_string
        string += 'In_b:\n' + In_b_string
        return string
        
    def display(self, **kwargs):
        return disp(self, **kwargs)

    def help(self):
        return __doc__