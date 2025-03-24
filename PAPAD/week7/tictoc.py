from pyomo.common.timing import TicTocTimer
from RandomizedModel import create_warehouse_model, solve_warehouse_location

timer = TicTocTimer()
timer.tic("start")
m = create_warehouse_model(num_locations=200, num_customers=200)
timer.toc("Build model")
solve_warehouse_location(m)
timer.toc("Wrote LP file and solved")