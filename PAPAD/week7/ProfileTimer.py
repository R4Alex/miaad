from RandomizedModel import *
import cProfile
import pstats

pr = cProfile.Profile()
pr.enable()
solve_parametric()
pr.disable()
print_c_profiler(pr)
