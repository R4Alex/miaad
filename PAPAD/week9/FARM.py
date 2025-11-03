from pyomo.environ import *

# Model definition
# Farm production planning over five years

def build_model():
    model = ConcreteModel()

    # Sets
    model.T = RangeSet(1,5)                # Years
    model.L = RangeSet(1,4)                # Land groups
    model.K = RangeSet(1,12)               # Cow ages (1=1-year-old, ..., 12=12-year-old)

    # Parameters
    model.housing_cap = Param(initialize=130)        # initial housing capacity (cows)
    model.land_cap    = Param(initialize=200)        # total land (acres)
    model.labor_cap   = Param(initialize=5500)       # regular labor hours available per year

    # Mortality and birth rates
    model.hf_decay    = Param(initialize=0.05)       # heifer mortality rate
    model.cow_decay   = Param(initialize=0.02)       # cow mortality rate
    model.birth_rate  = Param(initialize=1.1)        # calves per cow per year

    # Feed intake (tons per cow per year)
    model.gr_intake   = Param(initialize=0.6)
    model.sb_intake   = Param(initialize=0.7)

    # Agricultural yields and available area
    gr_yields = {1:1.10, 2:0.90, 3:0.80, 4:0.65}
    gr_areas  = {1:20,   2:30,   3:20,   4:10}
    model.gr_yield = Param(model.L, initialize=gr_yields)
    model.gr_area  = Param(model.L, initialize=gr_areas)
    model.sb_yield = Param(initialize=1.5)           # sugar beet yield (tons/acre)

    # Labor requirements (hours per unit)
    model.hf_labor = Param(initialize=10)
    model.cow_labor = Param(initialize=42)
    model.gr_labor = Param(initialize=4)
    model.sb_labor = Param(initialize=14)

    # Costs and prices
    model.price_bull   = Param(initialize=30)
    model.price_hf     = Param(initialize=40)
    model.price_cow    = Param(initialize=120)
    model.price_milk   = Param(initialize=370)
    model.price_sb_sell= Param(initialize=58)
    model.price_sb_buy = Param(initialize=70)
    model.price_gr_sell= Param(initialize=75)
    model.price_gr_buy = Param(initialize=90)
    model.cost_hf      = Param(initialize=50)
    model.cost_cow     = Param(initialize=100)
    model.cost_sb_land = Param(initialize=10)
    model.cost_gr_land = Param(initialize=15)
    model.reg_labor_cost = Param(initialize=4000)    # regular labor cost/year
    model.ot_labor_cost  = Param(initialize=1.20)    # overtime cost/hour

    # Loan installment (200 USD per additional cow slot)
    r = 0.15; n = 10; loan = 200
    inst = loan * r * (1+r)**n / ((1+r)**n - 1)
    model.installment = Param(initialize=inst)

    # Initial herd: 10 cows of each age
    init = {k: 10 for k in model.K}
    model.init_cows = Param(model.K, initialize=init)

    # Final herd size bounds (50% decrease, 75% increase)
    total_init = sum(init.values())
    model.min_final = Param(initialize=0.5 * total_init)
    model.max_final = Param(initialize=1.75 * total_init)

    # Decision variables
    model.Outlay   = Var(model.T, within=NonNegativeIntegers)
    model.Overtime= Var(model.T, within=NonNegativeReals)
    model.Newborn = Var(model.T, within=NonNegativeReals)
    model.HF_sell = Var(model.T, within=NonNegativeReals)
    model.SB_buy  = Var(model.T, within=NonNegativeReals)
    model.SB_sell = Var(model.T, within=NonNegativeReals)
    model.GR_buy  = Var(model.T, within=NonNegativeReals)
    model.GR_sell = Var(model.T, within=NonNegativeReals)
    model.SB      = Var(model.T, within=NonNegativeReals)
    model.GR      = Var(model.T, model.L, within=NonNegativeReals)
    model.Cows    = Var(model.T, model.K, within=NonNegativeReals)

    # Profit expression per year
    def profit_expr(m, t):
        milk_rev  = m.price_milk * sum(m.Cows[t,k] for k in m.K if k not in (1,12))
        bull_rev  = m.price_bull * 0.5 * m.birth_rate * sum(m.Cows[t,k] for k in m.K if k not in (1,12))
        hf_rev    = m.price_hf * m.HF_sell[t]
        cow_rev   = m.price_cow * m.Cows[t,12]
        sell_rev  = m.price_sb_sell*m.SB_sell[t] + m.price_gr_sell*m.GR_sell[t]
        hf_cost   = m.cost_hf * (m.Newborn[t] + m.Cows[t,1])
        cow_cost  = m.cost_cow * sum(m.Cows[t,k] for k in m.K if k not in (1,12))
        land_cost = m.cost_sb_land*m.SB[t] + m.cost_gr_land*sum(m.GR[t,l]/m.gr_yield[l] for l in m.L)
        labor_cost= m.reg_labor_cost + m.ot_labor_cost*m.Overtime[t]
        buy_cost  = m.price_sb_buy*m.SB_buy[t] + m.price_gr_buy*m.GR_buy[t]
        return milk_rev + bull_rev + hf_rev + cow_rev + sell_rev - (hf_cost + cow_cost + land_cost + labor_cost + buy_cost)
    model.Profit = Expression(model.T, rule=profit_expr)

    # Objective: maximize net profit minus loan payments
    model.obj = Objective(expr=sum(model.Profit[t] - model.installment*(t+4)*model.Outlay[t] for t in model.T), sense=maximize)

    # Constraints
    # 1. Housing capacity
    def housing_rule(m, t):
        return m.Newborn[t] + sum(m.Cows[t,k] for k in m.K if k!=12) <= m.housing_cap + sum(m.Outlay[d] for d in m.T if d<=t)
    model.HousingCap = Constraint(model.T, rule=housing_rule)

    # 2. Feeding constraints
    def grain_feed(m, t):
        return m.gr_intake * sum(m.Cows[t,k] for k in m.K if k not in (1,12)) <= m.GR_buy[t] - m.GR_sell[t] + sum(m.GR[t,l] for l in m.L)
    model.GrainFeed = Constraint(model.T, rule=grain_feed)

    def beet_feed(m, t):
        return m.sb_intake * sum(m.Cows[t,k] for k in m.K if k not in (1,12)) <= m.SB_buy[t] - m.SB_sell[t] + m.SB[t]
    model.BeetFeed = Constraint(model.T, rule=beet_feed)

    # 3. Agricultural production limits
    model.GRYield = Constraint(model.T, model.L,
        rule=lambda m, t, l: m.GR[t,l] <= m.gr_yield[l]*m.gr_area[l])

    # 4. Land use
    def land_use(m, t):
        return (m.SB[t]/m.sb_yield
                + (m.Newborn[t] + m.Cows[t,1])*(2/3)
                + sum(m.Cows[t,k] for k in m.K if k not in (1,12))
                + sum(m.GR[t,l]/m.gr_yield[l] for l in m.L)) <= m.land_cap
    model.LandUse = Constraint(model.T, rule=land_use)

    # 5. Labor use
    def labor_use(m, t):
        work = m.hf_labor*(m.Newborn[t] + m.Cows[t,1])
        work += m.cow_labor*sum(m.Cows[t,k] for k in m.K if k not in (1,12))
        work += sum(m.gr_labor*(m.GR[t,l]/m.gr_yield[l]) for l in m.L)
        work += m.sb_labor*(m.SB[t]/m.sb_yield)
        return work <= m.labor_cap + m.Overtime[t]
    model.LaborUse = Constraint(model.T, rule=labor_use)

    # 6. Herd dynamics
    # Initial herd
    def init_herd(m, k):
        return m.Cows[1,k] == m.init_cows[k]
    model.InitHerd = Constraint(model.K, rule=init_herd)
    # Age 1 (yearling) from newborns
    def herd_age1(m, t):
        if t == 1: return Constraint.Skip
        return m.Cows[t,1] == (1 - m.hf_decay)*m.Newborn[t-1]
    model.HerdAge1 = Constraint(model.T, rule=herd_age1)
    # Age 2 from yearlings
    def herd_age2(m, t):
        if t == 1: return Constraint.Skip
        return m.Cows[t,2] == (1 - m.hf_decay)*m.Cows[t-1,1]
    model.HerdAge2 = Constraint(model.T, rule=herd_age2)
    # Ages 3-12 from adult cows
    def herd_ages(m, t, k):
        if t == 1 or k < 3: return Constraint.Skip
        return m.Cows[t,k] == (1 - m.cow_decay)*m.Cows[t-1,k-1]
    model.HerdAges = Constraint(model.T, model.K, rule=herd_ages)

    # 7. Births and heifer sales
    def birth_sell(m, t):
        return m.Newborn[t] + m.HF_sell[t] == 0.5*m.birth_rate*sum(m.Cows[t,k] for k in m.K if k not in (1,12))
    model.BirthSell = Constraint(model.T, rule=birth_sell)

    # 8. Final herd size bounds
    def final_herd(m):
        total = sum(m.Cows[5,k] for k in m.K if k not in (1,12))
        return inequality(m.min_final, total, m.max_final)
    model.FinalHerd = Constraint(rule=final_herd)

    return model


if __name__ == '__main__':
    model = build_model()
    solver = SolverFactory('glpk')
    # results = solver.solve(model, tee=True)
    results = solver.solve(model)
    # Display optimal results
    print("\nOptimal total profit:", value(model.obj))

    # Less datails
    # for t in model.T:
    #     print(f"Year {t}: Outlay={value(model.Outlay[t])}, Overtime={value(model.Overtime[t])}, Newborn={value(model.Newborn[t])}, HF_sell={value(model.HF_sell[t])}")
    
    # Show more details
    for t in model.T:
        print(f'\nYear {t}: Outlay={value(model.Outlay[t])}, '
            f'Overtime={value(model.Overtime[t])}, '
            f'Newborn={value(model.Newborn[t])}, '
            f'HF_sell={value(model.HF_sell[t])}')
        print(f'  SB_buy={value(model.SB_buy[t])}, SB_sell={value(model.SB_sell[t])}')
        print(f'  GR_buy={value(model.GR_buy[t])}, GR_sell={value(model.GR_sell[t])}')
        print(f'  SB_cultivated={value(model.SB[t])}')
        for l in model.L:
            print(f'    GR_cultivated_group{l}={value(model.GR[t,l])}')