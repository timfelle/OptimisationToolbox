'''
KKT Based QP solver
'''

import sys
import numpy as np
from scipy.linalg import ldl,inv

def QP_solver(problem):
    # Function designed to select the appropriate solver used for a QP.

    H = problem.H
    A = problem.Eq_A
    Z = np.matrix(np.zeros( (problem.Eq_A.shape[1],problem.Eq_A.shape[1])))

    problem.kkt = np.block([ [H,-A], [-A.T,Z] ]) 
    problem.rhs = np.block([ [ - problem.g], [- problem.Eq_b] ])
    

    x_opt, f_opt = equality_LDL(problem)
    
    
    return x_opt,f_opt


def equality_LDL(problem):
    # Solution of Equality constrained QP

    L,D,p = ldl(problem.kkt)
    
    y = inv(L.T)*( inv(D)*( inv(L)*problem.rhs[p] ) )
    x_opt = np.matrix(y[0:problem.dim])
    f_opt = problem.f(x_opt.T)
    return x_opt, f_opt


