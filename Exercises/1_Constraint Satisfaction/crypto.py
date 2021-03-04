import matplotlib as mpl
import matplotlib.pyplot as plt

# from util import displayBoard
from itertools import product
from IPython.display import display
from z3 import *

ca_solver = Solver()  # create an instance of a Z3 CSP solver

#   T W O  :    9 3 8
# + T W O  :  + 9 3 8
# -------  :  -------
# F O U R  :  1 8 7 6

F = Int('F')  # create an z3.Int type variable instance called "F"
O = Int('O')
U = Int('U')
R = Int('R')
T = Int('T')
W = Int('W')
ca_solver.add(0 <= F, F <= 9)  # add constraints to the solver: 0 <= F <= 9
ca_solver.add(0 <= O, O <= 9)
ca_solver.add(0 <= U, U <= 9)
ca_solver.add(0 <= R, R <= 9)
ca_solver.add(0 <= T, T <= 9)
ca_solver.add(0 <= W, W <= 9)

# 1) leading digits cannot be zero
ca_solver.add(T != 0)
ca_solver.add(F != 0)

# 2) no two distinct letters represent the same digits
ca_solver.add(Distinct(F, O, U, R, T, W))

# Add any required variables and/or constraints to solve the cryptarithmetic puzzle
# Primary solution using single constraint for the cryptarithmetic equation
#  𝑇×10^2 + 𝑊×10^1 + 𝑂×10^0 + 𝑇×10^2 + 𝑊×10^1 + 𝑂×10^0 = 𝐹×10^3 + 𝑂×10^2 + 𝑈×10^1 + 𝑅×10^0

ca_solver.add((T * 10 ** 2 + W * 10 ** 1 + O * 10 ** 0 + T * 10 ** 2 + W * 10 ** 1 + O * 10 ** 0) == F * 10 ** 3 + O * 10 ** 2 + U * 10 ** 1 + R * 10 ** 0)

# Alternate solution using column-wise sums with carry values
c10 = Int('c10')
c100 = Int('c100')
c1000 = Int('c1000')
ca_solver.add(*[And(c >= 0, c <= 9) for c in [c10, c100, c1000]])
ca_solver.add(O + O == R + 10 * c10)
ca_solver.add(W + W + c10 == U + 10 * c100)
ca_solver.add(T + T + c100 == O + 10 * c1000)
ca_solver.add(F == c1000)

assert ca_solver.check() == sat, "Uh oh...the solver did not find a solution. Check your constraints."
print("  T W O  :    {} {} {}".format(ca_solver.model()[T], ca_solver.model()[W], ca_solver.model()[O]))
print("+ T W O  :  + {} {} {}".format(ca_solver.model()[T], ca_solver.model()[W], ca_solver.model()[O]))
print("-------  :  -------")
print("F O U R  :  {} {} {} {}".format(ca_solver.model()[F], ca_solver.model()[O], ca_solver.model()[U], ca_solver.model()[R]))
