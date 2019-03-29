'''
KKT Based QP solver
'''

import sys
import numpy as np

from .Solvers.QP import *

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

    return x_opt,f_opt

