'''
Main function for solving Linear programs.
'''

from .Solvers.LP import *

# =============================================================================
# Main function

def LP_solver(problem,**kwargs):
    # Function designed to select the appropriate solver used for a QP.

    N_eq = problem.Eq_b.size
    N_in = problem.In_b.size

    x_opt = f_opt = []

    # Unconstrained solution

    return x_opt,f_opt

