import numpy as np

def backTrackingLineSearch(problem,x_init=[],k_max=1e3,rho=0.9,c=0.1):
    
    if len(x_init) == 0: 
        x_init = np.matrix(np.zeros(problem.dim)).T

    k         = 0
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
