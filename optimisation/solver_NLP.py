'''
KKT Based QP solver
'''

import sys
import numpy as np
import time
from scipy.linalg import ldl,inv

# =============================================================================
# Main function

def NLP_solver(problem,**kwargs):
    # Function designed to select the appropriate solver used for a QP.

    N_eq = problem.Eq_b.size
    N_in = problem.In_b.size

    x_opt = f_opt = []

    # Unconstrained solution
    x_opt,f_opt = backTrackingLineSearch(problem,**kwargs)

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

def backTrackingLineSearch(problem,x_init=[0.0,0.0],k_max=1e3):
    k       = 0
    rho     = 0.9
    c       = 0.1

    tol       = 1e-6
    converged = False

    x   = np.matrix(x_init).T
    x_list = +x

    while not converged and k < k_max:

        alpha = 1.0
        f       = problem.f(x)
        df      = -problem.Df(x)

        x_tmp  = x + df
        f_tmp  = problem.f(x_tmp)

        while f_tmp >= f - c * df.T * df:
            alpha *= rho
            x_tmp = x + alpha * df
            f_tmp  = problem.f(x_tmp)

        x = +x_tmp

        k += 1
        converged = np.linalg.norm(df) < tol
        x_list = np.hstack((x_list,x))
    

    problem.x_list = x_list
    x_opt = x
    f_opt = problem.f(x_opt)
    
    return x_opt, f_opt



# =============================================================================
# General functions
