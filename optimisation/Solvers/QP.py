# =============================================================================
# This file creates a full list of solvers for Qudratic programming.
# When new algorithms are implemented add them to this list to enable use in the
# main solver.

# Linear Equality Constraints
from .QP_equality_LDL import equality_LDL