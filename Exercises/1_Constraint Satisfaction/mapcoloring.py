import matplotlib as mpl
import matplotlib.pyplot as plt

# from util import displayBoard
from itertools import product
from IPython.display import display
from z3 import *

# create instance of Z3 solver & declare color palette
mc_solver = Solver()
colors = {'0': "Blue", '1': "Red", '2': "Green"}

#WA=Western Australia, SA=Southern Australia, NT=Northern Territory, Q=Queensland, NSW=New South Wales, V=Victoria, T=Tasmania
WA = Int('WA')
mc_solver.add(0 <= WA, WA <= 2)
SA = Int('SA')
mc_solver.add(0 <= SA, SA <= 2)
NT = Int('NT')
mc_solver.add(0 <= NT, NT <= 2)
Q = Int('Q')
mc_solver.add(0 <= Q, Q <= 2)
V = Int('V')
mc_solver.add(0 <= V, V <= 2)
T = Int('T')
mc_solver.add(0 <= T, T <= 2)
NSW = Int('NSW')
mc_solver.add(0 <= NSW, NSW <= 2)

# constraints to require adjacent regions to take distinct colors
# Primary solution: use pseudo-boolean k-ary constraints (0 of k can be True => all constraints are False)
mc_solver.add(PbEq(((WA==NT, 1), (WA==SA, 1)), 0))
mc_solver.add(PbEq(((NT==WA, 1), (NT==SA, 1), (NT==Q, 1)), 0))
mc_solver.add(PbEq(((SA==WA, 1), (SA==NT, 1), (SA==Q, 1), (SA==NSW, 1), (SA==V, 1)), 0))
mc_solver.add(PbEq(((Q==NT, 1), (Q==SA, 1), (Q==NSW, 1)), 0))
mc_solver.add(PbEq(((NSW==SA, 1), (NSW==Q, 1), (NSW==V, 1)), 0))
mc_solver.add(PbEq(((V==SA, 1), (V==NSW, 1)), 0))

# Alternate solution: binary constraints for each pair of adjacent territories
adjacency = {WA: [NT, SA], NT: [WA, SA, Q], SA: [WA, NT, Q, NSW, V], Q: [NT, SA, NSW], NSW: [SA, Q, V], V: [SA, NSW]}
for rA in adjacency:
    for rB in adjacency[rA]:
        mc_solver.add(rA != rB)

assert mc_solver.check() == sat, "Uh oh. The solver failed to find a solution. Check your constraints."
print("WA={}".format(colors[mc_solver.model()[WA].as_string()]))
print("NT={}".format(colors[mc_solver.model()[NT].as_string()]))
print("SA={}".format(colors[mc_solver.model()[SA].as_string()]))
print("Q={}".format(colors[mc_solver.model()[Q].as_string()]))
print("NSW={}".format(colors[mc_solver.model()[NSW].as_string()]))
print("V={}".format(colors[mc_solver.model()[V].as_string()]))
print("T={}".format(colors[mc_solver.model()[T].as_string()]))
