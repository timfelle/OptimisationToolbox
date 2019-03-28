'''
KKT Based QP solver
'''

import sys
import numpy as np
import time
from .solver_NLP import NLP_solver
from scipy.linalg import ldl,inv

# =============================================================================
# Main function

def QP_solver(problem,**kwargs):
    # Function designed to select the appropriate solver used for a QP.

    N_eq = problem.Eq_b.size
    N_in = problem.In_b.size

    x_opt = f_opt = []

    if ( (N_in == 0 and N_eq != 0) and
        ( 'PositiveDefinite' in problem.definite )):  
        x_opt, f_opt = equality_LDL(problem,**kwargs)
    else:
        x_opt, f_opt = NLP_solver(problem)


    # Prints warning if no suitable solver was found for the problem.
    if len(x_opt) == 0:
        W  = '-------------------------------------------------------------\n' 
        W += '| WARNING:                                                  |\n'
        W += '|   No suitable solver found.                               |\n'
        W += '-------------------------------------------------------------'
        print(W,file=sys.stderr)
        
    return x_opt,f_opt


# =============================================================================
# Solvers

def equality_LDL(problem):
    # Solution of Equality constrained QP via a LDL factorisation of the KKT 
    # Matrix.

    kkt, rhs = _KKT(problem)
    L,D,p = ldl(kkt)
    
    y   = inv(L.T)*( inv(D)*( inv(L)*rhs[p] ) )
    x   = np.matrix(y[0:problem.dim])
    lam = np.matrix(y[problem.dim:])

    # Check if solution exists and satisfy the constraints
    for l in lam: 
        if l != 0: 
            print('Satisfied')

    x_opt = x
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

