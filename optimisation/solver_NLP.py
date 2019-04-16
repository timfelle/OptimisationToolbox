'''
Main function for solving Non Linear programs.
'''

from .Solvers.NLP import *


# =============================================================================
# Main function

def NLP_solver(problem,**kwargs):
    # Function designed to select the appropriate solver used for a QP.

    N_eq = problem.Eq_b.size
    N_in = problem.In_b.size

    x_opt = f_opt = []

    # Unconstrained solution
    if N_eq == 0 and N_in == 0:
        x_opt,f_opt = backTrackingLineSearch(problem,**kwargs)

    return x_opt,f_opt