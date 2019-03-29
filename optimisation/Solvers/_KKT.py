import numpy as np


def KKT(problem):
    # Sets up the KKT and RHS systems
    
    H = problem.H
    A = problem.Eq_A
    Z = np.matrix(np.zeros( (problem.Eq_A.shape[1],problem.Eq_A.shape[1])))

    kkt = np.block([ [H,-A], [-A.T,Z] ]) 
    rhs = np.block([ [ - problem.g], [- problem.Eq_b] ])

    return kkt, rhs
