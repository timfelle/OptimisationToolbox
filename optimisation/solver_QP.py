'''
KKT Based QP solver
'''

import sys
import numpy as np
from scipy.linalg import ldl,inv

# =============================================================================
# Main function

def QP_solver(problem):
    # Function designed to select the appropriate solver used for a QP.

    N_eq = problem.Eq_b.size
    N_in = problem.In_b.size
    print( problem.Eq_b )
    print( problem.In_b )
    x_opt = f_opt = []

    if ( (N_in == 0 and N_eq != 0) and
        ( 'PositiveDefinite' in problem.definite )
    ):  x_opt, f_opt = equality_LDL(problem)
    
    else:
        print('Solver not implemented', file=sys.stderr)
        exit()
    
    return x_opt,f_opt


# =============================================================================
# Solvers

def equality_LDL(problem):
    # Solution of Equality constrained QP via a LDL factorisation of the KKT 
    # Matrix.

    kkt, rhs = _KKT(problem)
    L,D,p = ldl(kkt)
    
    y = inv(L.T)*( inv(D)*( inv(L)*rhs[p] ) )
    x_opt = np.matrix(y[0:problem.dim])
    f_opt = problem.f(x_opt.T)



    return x_opt, f_opt


# =============================================================================
# General functions

def _KKT(problem):
    # Sets up the KKT and RHS systems
    
    H = problem.H
    A = problem.Eq_A
    Z = np.matrix(np.zeros( (problem.Eq_A.shape[1],problem.Eq_A.shape[1])))

    kkt = np.block([ [H,-A], [-A.T,Z] ]) 
    rhs = np.block([ [ - problem.g], [- problem.Eq_b] ])

    return kkt, rhs

