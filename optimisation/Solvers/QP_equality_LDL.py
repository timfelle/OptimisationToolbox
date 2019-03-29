import numpy as np
from ._KKT import KKT
from scipy.linalg import ldl,inv

def equality_LDL(problem):
    # Solution of Equality constrained QP via a LDL factorisation of the KKT 
    # Matrix.

    kkt, rhs = KKT(problem)
    L,D,p = ldl(kkt)
    
    y   = inv(L.T)*( inv(D)*( inv(L)*rhs[p] ) )
    x   = np.matrix(y[0:problem.dim])
    lam = np.matrix(y[problem.dim:])

    # Check if solution exists and satisfy the constraints
    for l in lam: 
        if l != 0: 
            print('Satisfied')

    x_opt = x
    f_opt = problem.f(x_opt)


    return x_opt, f_opt