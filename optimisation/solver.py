'''
KKT Based QP solver
'''

import sys
import numpy as np
from .solver_NLP import NLP_solver
from .solver_QP import QP_solver
from .solver_LP import LP_solver

# =============================================================================
# Main function

def solver(problem, **kwargs):
    # Function designed to select the appropriate solver used for a QP.
    Type = problem.type

    x_opt = f_opt = []

    if Type == 'QP':
        x_opt, f_opt = QP_solver(problem, **kwargs)
    elif Type == 'LP':
        x_opt, f_opt = LP_solver(problem, **kwargs)
    else:
        x_opt, f_opt = NLP_solver(problem, **kwargs)


    # Prints warning if no suitable solver was found for the problem.
    if len(x_opt) == 0:
        W  = '-------------------------------------------------------------\n' 
        W += '| WARNING:                                                  |\n'
        W += '|   No suitable solver found.                               |\n'
        W += '-------------------------------------------------------------'
        print(W,file=sys.stderr)
        
    return x_opt,f_opt

