import optimisation
import numpy as np

sep = '========================================================================'

# Define the matrices used in all

H = np.matrix([[ 2, 0 ],[0,2]])
g = np.matrix( [-2, -5 ] ).T

Eq_A = np.matrix([[ 1, 2]]).T
Eq_b = np.matrix([[ 2 ]]).T

In_A = np.matrix([[1,-2],[-1,-2], [-1,2], [1,0], [0,1]]).T
In_b = np.matrix([[ -2, -6, -2, 0, 0 ]]).T

A2 = [ [1,-1], [1,1] ]
b2 = [0,1]
print(sep)
# =============================================================================
# Setting up and testing functions related to QP
QP = optimisation.QP(
    H,g,
    Eq_A = Eq_A, Eq_b = Eq_b,
    In_A = In_A, In_b = In_b
    )

#QP.help()

QP.add_constraints(In_A=A2,In_b=b2)

QP.print()


QP.solve()

QP.print()
QP.display(x_lim=[-0.5,5], y_lim=[-0.5,3], obj_levels=50, display=True)

exit()
print(sep)
# =============================================================================
# Setting up and testing functions related to LP

# Define the problem
LP = optimisation.LP(
    g,
    Eq_A = Eq_A, Eq_b = Eq_b,
    In_A = In_A, In_b = In_b
    )

LP.help()

LP.add_constraints(In_A=A2,In_b=b2)

LP.print()

LP.display(x_lim=[-0.5,5], y_lim=[-0.5,3], obj_levels=50)

print(sep)
# =============================================================================
# Setting up and testing functions related to NLP
NLP = optimisation.NLP(
    lambda x: x[0]**3 + x[1]**2 + x[0], 2,
    Eq_A = Eq_A, Eq_b = Eq_b,
    In_A = In_A, In_b = In_b
    )

NLP.help()

NLP.add_constraints(In_A=A2,In_b=b2)

NLP.print()

NLP.display(x_lim=[-0.5,5], y_lim=[-0.5,3], obj_levels=50)
