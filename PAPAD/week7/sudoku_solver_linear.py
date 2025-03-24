import pyomo.environ as pyo
from pyomo.core.expr.numeric_expr import LinearExpression

# Create a standard python dict for mapping subsquares to the list [row, col] entries
subsq_to_row_col = dict()
subsq_to_row_col[1] = [(i,j) for i in range(1,4) for j in range(1,4)]
subsq_to_row_col[2] = [(i,j) for i in range(1,4) for j in range(4,7)]
subsq_to_row_col[3] = [(i,j) for i in range(1,4) for j in range(7,10)]
subsq_to_row_col[4] = [(i,j) for i in range(4,7) for j in range(1,4)]
subsq_to_row_col[5] = [(i,j) for i in range(4,7) for j in range(4,7)]
subsq_to_row_col[6] = [(i,j) for i in range(4,7) for j in range(7,10)]
subsq_to_row_col[7] = [(i,j) for i in range(7,10) for j in range(1,4)]
subsq_to_row_col[8] = [(i,j) for i in range(7,10) for j in range(4,7)]
subsq_to_row_col[9] = [(i,j) for i in range(7,10) for j in range(7,10)]

# Creates the sudoku model for a 9x9 board, where the input board is a list of fixed numbers specified in (row, col, val) tuples.
def create_sudoku_model(board):
    model = pyo.ConcreteModel()

    # Store the starting board for the model
    model.board = board

    # Create sets for rows, columns and squares
    model.ROWS = pyo.RangeSet(1,9)
    model.COLS = pyo.RangeSet(1,9)
    model.SUBSQUARES = pyo.RangeSet(1,9)
    model.VALUES = pyo.RangeSet(1,9)

    # Create the binary variables to define the values
    model.y = pyo.Var(model.ROWS, model.COLS, model.VALUES, within=pyo.Binary)

    # Fix variables based on the current board
    for r, c, v in board:
        model.y[r, c, v].fix(1)

    # Create the objective - this is a feasibility problem so we just make it a constant
    model.obj = pyo.Objective(expr=1.0)



    # for i in range(N2):
    #     e = sum(i * m.x[i] for i in range(N1))
    # timer.toc('created expression with sum function')

    # for i in range(N2):
    #     coefs = [i for i in range(N1)]
    #     lin_vars = [m.x[i] for i in range(N1)]
    #     e = LinearExpression(constant=0, linear_coefs=coefs, linear_vars=lin_vars)


    # Constraint: exactly one number in each row
    def _RowCon(model, r, v):
        # return sum(model.y[r, c, v] for c in model.COLS) == 1
        coefs = [1 for i in range(9)]
        lin_vars = [model.y[r, c, v] for c in model.COLS]
        return LinearExpression(constant=0, linear_coefs=coefs, linear_vars=lin_vars) == 1
    
    model.RowCon = pyo.Constraint(model.ROWS, model.VALUES, rule=_RowCon)

    # Constraint: exactly one number in each column
    def _ColCon(model, c, v):
        # return sum(model.y[r, c, v] for r in model.ROWS) == 1
        coefs = [1 for i in range(9)]
        lin_vars = [model.y[r, c, v] for r in model.ROWS]
        return LinearExpression(constant=0, linear_coefs=coefs, linear_vars=lin_vars) == 1

    model.ColCon = pyo.Constraint(model.COLS, model.VALUES, rule=_ColCon)

    # Constraint: exactly one number in each subsquare
    def _SgCon(model, s, v):
        # return sum(model.y[r, c, v] for (r, c) in subsq_to_row_col[s]) == 1
        coefs = [1 for i in range(9)]
        lin_vars = [model.y[r, c, v] for (r, c) in subsq_to_row_col[s]]
        return LinearExpression(constant=0, linear_coefs=coefs, linear_vars=lin_vars) == 1

    model.SgCon = pyo.Constraint(model.SUBSQUARES, model.VALUES, rule=_SgCon)

    # Constraint: exactly one number in each cell
    def _ValueCon(model, r, c):
        # return sum(model.y[r, c, v] for v in model.VALUES) == 1
        coefs = [1 for i in range(9)]
        lin_vars = [model.y[r, c, v] for v in model.VALUES]
        return LinearExpression(constant=0, linear_coefs=coefs, linear_vars=lin_vars) == 1

    model.ValueCon = pyo.Constraint(model.ROWS, model.COLS, rule=_ValueCon)

    return model

# Use this function to add a new integer cut to the model.
def add_integer_cut(model):
    # Add the ConstraintList to store the IntegerCuts if it does not already exist
    if not hasattr(model, "IntegerCuts"):
        model.IntegerCuts = pyo.ConstraintList()
    
    # Add the integer cut corresponding to the current solution in the model
    cut_expr = 0.0
    for r in model.ROWS:
        for c in model.COLS:
            for v in model.VALUES:
                if not model.y[r, c, v].fixed:
                    # Check if the binary variable is on or off
                    # Note, it may not be exactly 1
                    if pyo.value(model.y[r, c, v]) >= 0.5:
                        cut_expr += (1.0 - model.y[r, c, v])
                    else:
                        cut_expr += model.y[r, c, v]
    
    model.IntegerCuts.add(cut_expr >= 1)

# Prints the current solution stored in the model
def print_solution(model):
    for r in model.ROWS:
        print(' '.join(str(v) for c in model.COLS 
                        for v in model.VALUES 
                        if pyo.value(model.y[r, c, v]) >= 0.5))

from pyomo.opt import (SolverFactory, TerminationCondition)
# from sudoku import (create_sudoku_model, 
#                     print_solution, 
#                     add_integer_cut)

# Define the board
board = [(1,1,5), (1,2,3), (1,5,7), 
         (2,1,6), (2,4,1), (2,5,9), (2,6,5), 
         (3,2,9), (3,3,8), (3,8,6), 
         (4,1,8), (4,5,6), (4,9,3), 
         (5,1,4), (5,4,8), (5,6,3), (5,9,1), 
         (6,1,7), (6,5,2), (6,9,6), 
         (7,2,6), (7,7,2), (7,8,8), 
         (8,4,4), (8,5,1), (8,6,9), (8,9,5), 
         (9,5,8), (9,8,7), (9,9,9)]

model = create_sudoku_model(board)

solution_count = 0
while 1:
    with SolverFactory("glpk") as opt:
        results = opt.solve(model)

    if results.solver.termination_condition != \
       TerminationCondition.optimal:
        print("All board solutions have been found")
        break

    solution_count += 1

    add_integer_cut(model)

    print("Solution #%d" % (solution_count))
    print_solution(model)
