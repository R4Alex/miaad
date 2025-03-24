from RandomizedModel import create_warehouse_model
from pyomo.common.timing import report_timing
from pyomo.opt.results import assert_optimal_termination

report_timing()
print("Building model")
print("--------------")
m = create_warehouse_model(num_locations=200, num_customers=200)
